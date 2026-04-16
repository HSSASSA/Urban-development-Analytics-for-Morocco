"""
Comparative and statistical analysis
"""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
import logging
from typing import Dict, Tuple, List

class ComparativeAnalysis:
    """Comparative analysis across regions and cities"""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
    
    def regional_comparison(self, df: pd.DataFrame, metric: str, year: int = None) -> pd.DataFrame:
        """Compare metrics across regions"""
        self.logger.info(f"Performing regional comparison for {metric}")
        
        if year:
            df = df[df['year'] == year]
        
        regional_stats = df.groupby('region').agg({
            metric: ['mean', 'std', 'min', 'max', 'count']
        }).round(3)
        
        return regional_stats
    
    def temporal_analysis(self, df: pd.DataFrame, region: str = None) -> pd.DataFrame:
        """Analyze temporal trends"""
        self.logger.info(f"Performing temporal analysis for {region or 'all regions'}")
        
        if region:
            df = df[df['region'] == region]
        
        temporal_stats = df.groupby('year').agg({
            col: 'mean' for col in df.select_dtypes(include=['float64', 'int32', 'int64']).columns
            if col not in ['year', 'region']
        }).round(3)
        
        return temporal_stats
    
    def perform_ttest(self, df: pd.DataFrame, metric: str, 
                      group_col: str = 'city_type') -> Dict:
        """Perform t-test between groups"""
        self.logger.info(f"Performing t-test for {metric} grouped by {group_col}")
        
        groups = df[group_col].unique()
        results = {}
        
        for i, group1 in enumerate(groups):
            for group2 in groups[i+1:]:
                group1_data = df[df[group_col] == group1][metric].dropna()
                group2_data = df[df[group_col] == group2][metric].dropna()
                
                t_stat, p_value = stats.ttest_ind(group1_data, group2_data)
                
                results[f"{group1} vs {group2}"] = {
                    't_statistic': round(t_stat, 4),
                    'p_value': round(p_value, 4),
                    'significant': p_value < 0.05
                }
        
        return results
    
    def correlation_analysis(self, df: pd.DataFrame, numeric_cols: List[str] = None) -> pd.DataFrame:
        """Calculate correlation matrix"""
        self.logger.info("Performing correlation analysis")
        
        if numeric_cols is None:
            numeric_cols = df.select_dtypes(include=['float64', 'int32', 'int64']).columns.tolist()
        
        corr_matrix = df[numeric_cols].corr()
        
        return corr_matrix
    
    def identify_strong_correlations(self, corr_matrix: pd.DataFrame, 
                                    threshold: float = 0.7) -> List[Tuple]:
        """Identify strong correlations above threshold"""
        self.logger.info(f"Identifying correlations above {threshold}")
        
        strong_corr = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > threshold:
                    col1 = corr_matrix.columns[i]
                    col2 = corr_matrix.columns[j]
                    strong_corr.append((col1, col2, round(corr_value, 3)))
        
        return strong_corr


class AdvancedStatistics:
    """Advanced statistical analyses"""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
    
    def distribution_analysis(self, data: pd.Series) -> Dict:
        """Analyze data distribution"""
        self.logger.info("Analyzing distribution")
        
        # Normality test
        statistic, p_value = stats.normaltest(data.dropna())
        
        return {
            'mean': round(data.mean(), 3),
            'median': round(data.median(), 3),
            'std_dev': round(data.std(), 3),
            'skewness': round(stats.skew(data.dropna()), 3),
            'kurtosis': round(stats.kurtosis(data.dropna()), 3),
            'normality_p_value': round(p_value, 4),
            'is_normal': p_value > 0.05
        }
    
    def efficiency_frontier(self, df: pd.DataFrame, 
                           efficiency_col: str, 
                           cost_col: str = None) -> pd.DataFrame:
        """Identify efficiency frontier"""
        self.logger.info("Computing efficiency frontier")
        
        df_sorted = df.sort_values(by=efficiency_col, ascending=False).copy()
        
        if cost_col and cost_col in df.columns:
            df_sorted['efficiency_cost_ratio'] = df_sorted[efficiency_col] / (df_sorted[cost_col] + 1)
            df_sorted = df_sorted.sort_values(by='efficiency_cost_ratio', ascending=False)
        else:
            df_sorted['ranking'] = range(1, len(df_sorted) + 1)
        
        return df_sorted.head(10)
    
    def growth_analysis(self, df: pd.DataFrame, metric: str, 
                       group_col: str = 'region') -> pd.DataFrame:
        """Calculate growth rates"""
        self.logger.info(f"Analyzing growth for {metric}")
        
        growth_data = []
        
        for group in df[group_col].unique():
            group_df = df[df[group_col] == group].sort_values('year')
            
            if len(group_df) > 1:
                initial_value = group_df[metric].iloc[0]
                final_value = group_df[metric].iloc[-1]
                years = group_df['year'].iloc[-1] - group_df['year'].iloc[0]
                
                if years > 0:
                    cagr = (final_value / initial_value) ** (1/years) - 1
                    growth_data.append({
                        group_col: group,
                        'initial_value': round(initial_value, 2),
                        'final_value': round(final_value, 2),
                        'absolute_change': round(final_value - initial_value, 2),
                        'percent_change': round((final_value - initial_value) / initial_value * 100, 2),
                        'cagr': round(cagr * 100, 2)
                    })
        
        return pd.DataFrame(growth_data)
