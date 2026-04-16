"""
Unit tests for pipeline and analysis components
"""
import pytest
import pandas as pd
import numpy as np
from src.utils.data_generator import UrbanDataGenerator
from src.utils.validators import DataValidator
from src.pipeline.etl import ETLPipeline
from src.analysis.comparative_analysis import ComparativeAnalysis, AdvancedStatistics
from src.analysis.timeseries_forecasting import PredictiveModeling

class TestDataGenerator:
    """Test data generation functions"""
    
    def test_generate_urban_indicators(self):
        """Test urban indicators generation"""
        df = UrbanDataGenerator.generate_urban_indicators(n_records=100)
        
        assert len(df) == 100
        assert 'population' in df.columns
        assert 'gdp_per_capita' in df.columns
        assert df['population'].min() > 0
        assert df['gdp_per_capita'].min() > 0
    
    def test_generate_housing_data(self):
        """Test housing data generation"""
        df = UrbanDataGenerator.generate_housing_data(n_records=50)
        
        assert len(df) == 50
        assert 'housing_units_completed' in df.columns
        assert 'price_per_sqm_dirham' in df.columns
        assert df['vacancy_rate'].min() >= 0
        assert df['vacancy_rate'].max() <= 1
    
    def test_all_datasets_generated(self):
        """Test all datasets are generated correctly"""
        urban, housing, infra, migration = UrbanDataGenerator.generate_all_datasets()
        
        assert len(urban) > 0
        assert len(housing) > 0
        assert len(infra) > 0
        assert len(migration) > 0

class TestDataValidator:
    """Test data validation functions"""
    
    def test_check_nulls(self):
        """Test null value checking"""
        df = pd.DataFrame({
            'col1': [1, 2, None, 4],
            'col2': [None, None, None, None]
        })
        
        validator = DataValidator()
        is_valid, null_report = validator.check_nulls(df, max_null_pct=0.5)
        
        assert 'col1' in null_report
        assert null_report['col2'] == 1.0
    
    def test_check_duplicates(self):
        """Test duplicate detection"""
        df = pd.DataFrame({
            'id': [1, 2, 2, 3],
            'value': [10, 20, 20, 30]
        })
        
        validator = DataValidator()
        is_valid, dup_count = validator.check_duplicates(df, subset=['id', 'value'])
        
        assert dup_count == 1
    
    def test_detect_outliers(self):
        """Test outlier detection"""
        data = [1, 2, 3, 4, 5, 100]  # 100 is outlier
        df = pd.DataFrame({'values': data})
        
        validator = DataValidator()
        outliers = validator.detect_outliers(df, ['values'])
        
        assert outliers['values'] >= 1

class TestETLPipeline:
    """Test ETL pipeline"""
    
    def test_transform_urban_indicators(self):
        """Test urban indicators transformation"""
        df = UrbanDataGenerator.generate_urban_indicators(n_records=100)
        
        pipeline = ETLPipeline()
        transformed = pipeline.transform_urban_indicators(df)
        
        assert 'urbanization_rate' in transformed.columns
        assert 'housing_need_index' in transformed.columns
        assert not transformed['unemployment_rate'].isnull().any()
    
    def test_transform_housing(self):
        """Test housing data transformation"""
        df = UrbanDataGenerator.generate_housing_data(n_records=100)
        
        pipeline = ETLPipeline()
        transformed = pipeline.transform_housing(df)
        
        assert 'housing_completion_rate' in transformed.columns
        assert 'affordable_housing_ratio' in transformed.columns
        assert (transformed['housing_completion_rate'] >= 0).all()
        assert (transformed['housing_completion_rate'] <= 1).all()

class TestComparativeAnalysis:
    """Test comparative analysis"""
    
    def test_regional_comparison(self):
        """Test regional comparison"""
        df = UrbanDataGenerator.generate_urban_indicators(n_records=100)
        
        analysis = ComparativeAnalysis()
        regional_stats = analysis.regional_comparison(df, 'population')
        
        assert len(regional_stats) > 0
        assert ('population', 'mean') in regional_stats.columns
    
    def test_correlation_analysis(self):
        """Test correlation analysis"""
        df = UrbanDataGenerator.generate_urban_indicators(n_records=100)
        
        analysis = ComparativeAnalysis()
        corr_matrix = analysis.correlation_analysis(df)
        
        assert len(corr_matrix) > 0
        assert corr_matrix.iloc[0, 0] == 1.0  # Diagonal should be 1

class TestAdvancedStatistics:
    """Test advanced statistics"""
    
    def test_distribution_analysis(self):
        """Test distribution analysis"""
        data = pd.Series(np.random.normal(100, 15, 1000))
        
        stats = AdvancedStatistics()
        dist_analysis = stats.distribution_analysis(data)
        
        assert 'mean' in dist_analysis
        assert 'std_dev' in dist_analysis
        assert 'is_normal' in dist_analysis
    
    def test_growth_analysis(self):
        """Test growth analysis"""
        df = UrbanDataGenerator.generate_urban_indicators(n_records=100)
        
        stats = AdvancedStatistics()
        growth = stats.growth_analysis(df, 'population', 'region')
        
        assert len(growth) > 0
        assert 'cagr' in growth.columns

class TestPredictiveModeling:
    """Test predictive models"""
    
    def test_linear_trend_model(self):
        """Test linear trend fitting"""
        df = pd.DataFrame({
            'year': [2015, 2016, 2017, 2018, 2019, 2020],
            'value': [100, 105, 110, 115, 120, 125]
        })
        
        predictor = PredictiveModeling()
        results = predictor.linear_trend_model(df, 'value')
        
        assert 'overall' in results
        assert 'slope' in results['overall']
        assert results['overall']['slope'] > 0
    
    def test_forecast_trend(self):
        """Test trend forecasting"""
        df = pd.DataFrame({
            'year': [2015, 2016, 2017, 2018, 2019, 2020],
            'value': [100, 105, 110, 115, 120, 125]
        })
        
        predictor = PredictiveModeling()
        forecast = predictor.forecast_trend(df, 'value', years_ahead=3)
        
        assert len(forecast) == 3
        assert forecast['year'].min() == 2021
        assert forecast['year'].max() == 2023
    
    def test_scenario_analysis(self):
        """Test scenario analysis"""
        df = pd.DataFrame({
            'metric': [100, 105, 110, 115, 120]
        })
        
        scenarios = {'low': -0.05, 'medium': 0.03, 'high': 0.10}
        
        predictor = PredictiveModeling()
        results = predictor.scenario_analysis(df, 'metric', scenarios)
        
        assert len(results) == 3
        assert results['scenario'].tolist() == ['low', 'medium', 'high']

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
