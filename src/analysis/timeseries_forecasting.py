"""
Time series and predictive analysis
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import logging
from typing import Dict, Tuple

class TimeSeriesAnalysis:
    """Time series decomposition and forecasting"""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
    
    def calculate_moving_averages(self, df: pd.DataFrame, metric: str, 
                                  windows: list = [3, 5]) -> pd.DataFrame:
        """Calculate moving averages"""
        self.logger.info(f"Calculating moving averages for {metric}")
        
        df_sorted = df.sort_values('year').copy()
        
        for window in windows:
            df_sorted[f'ma_{window}'] = df_sorted[metric].rolling(window=window, center=True).mean()
        
        return df_sorted
    
    def seasonal_decomposition(self, df: pd.DataFrame, metric: str, 
                              group_col: str = 'region') -> Dict:
        """Detect seasonal patterns"""
        self.logger.info(f"Performing seasonal decomposition for {metric}")
        
        seasonal_patterns = {}
        
        for group in df[group_col].unique():
            group_data = df[df[group_col] == group].sort_values('year')
            
            # Group by month/quarter pattern
            seasonal_patterns[group] = {
                'trend': group_data[metric].mean(),
                'volatility': group_data[metric].std(),
                'coefficient_variation': group_data[metric].std() / (group_data[metric].mean() + 1)
            }
        
        return seasonal_patterns


class PredictiveModeling:
    """Machine learning models for forecasting"""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.models = {}
        self.scaler = StandardScaler()
    
    def prepare_timeseries_data(self, df: pd.DataFrame, metric: str, 
                               lag: int = 3) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare data for time series modeling"""
        self.logger.info(f"Preparing time series data with lag={lag}")
        
        df_sorted = df.sort_values('year')
        values = df_sorted[metric].values
        
        X, y = [], []
        for i in range(len(values) - lag):
            X.append(values[i:i+lag])
            y.append(values[i+lag])
        
        return np.array(X), np.array(y)
    
    def linear_trend_model(self, df: pd.DataFrame, metric: str, 
                          group_col: str = None) -> Dict:
        """Fit linear trend model"""
        self.logger.info(f"Fitting linear trend model for {metric}")
        
        results = {}
        
        if group_col:
            for group in df[group_col].unique():
                group_df = df[df[group_col] == group].sort_values('year')
                X = group_df[['year']].values
                y = group_df[metric].values
                
                model = LinearRegression()
                model.fit(X, y)
                
                results[group] = {
                    'slope': round(model.coef_[0], 4),
                    'intercept': round(model.intercept_, 2),
                    'r_squared': round(model.score(X, y), 4)
                }
        else:
            X = df[['year']].values
            y = df[metric].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            results['overall'] = {
                'slope': round(model.coef_[0], 4),
                'intercept': round(model.intercept_, 2),
                'r_squared': round(model.score(X, y), 4)
            }
        
        return results
    
    def forecast_trend(self, df: pd.DataFrame, metric: str, 
                      years_ahead: int = 5) -> pd.DataFrame:
        """Forecast future values based on trend"""
        self.logger.info(f"Forecasting {metric} for {years_ahead} years ahead")
        
        df_sorted = df.sort_values('year')
        X = df_sorted[['year']].values
        y = df_sorted[metric].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        last_year = df_sorted['year'].max()
        future_years = np.arange(last_year + 1, last_year + years_ahead + 1).reshape(-1, 1)
        
        forecasts = model.predict(future_years)
        
        forecast_df = pd.DataFrame({
            'year': future_years.flatten(),
            f'{metric}_forecast': forecasts.round(2),
            'forecast_type': 'linear_trend'
        })
        
        return forecast_df
    
    def random_forest_forecast(self, df: pd.DataFrame, metric: str, 
                              features: list, test_size: float = 0.2) -> Dict:
        """Build random forest model for prediction"""
        self.logger.info(f"Training random forest model for {metric}")
        
        # Prepare data
        df_clean = df.dropna(subset=features + [metric])
        X = df_clean[features]
        y = df_clean[metric]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        self.models[metric] = model
        
        return {
            'r2_score': round(r2, 4),
            'mae': round(mae, 2),
            'rmse': round(rmse, 2),
            'feature_importance': feature_importance.to_dict('records')
        }
    
    def scenario_analysis(self, df: pd.DataFrame, metric: str, 
                         scenarios: Dict) -> pd.DataFrame:
        """Perform scenario analysis with different assumptions"""
        self.logger.info(f"Performing scenario analysis for {metric}")
        
        base_value = df[metric].iloc[-1]
        results = []
        
        for scenario_name, growth_rate in scenarios.items():
            projected_values = [base_value]
            
            for year in range(1, 6):
                projected_values.append(projected_values[-1] * (1 + growth_rate))
            
            results.append({
                'scenario': scenario_name,
                'year_0': round(projected_values[0], 2),
                'year_1': round(projected_values[1], 2),
                'year_3': round(projected_values[3], 2),
                'year_5': round(projected_values[5], 2),
            })
        
        return pd.DataFrame(results)
