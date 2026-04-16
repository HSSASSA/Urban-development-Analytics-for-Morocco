"""
Initialize analysis package
"""
from src.pipeline.etl import ETLPipeline
from src.analysis.comparative_analysis import ComparativeAnalysis, AdvancedStatistics
from src.analysis.timeseries_forecasting import TimeSeriesAnalysis, PredictiveModeling
from src.utils.config import setup_logging, load_config
from src.utils.validators import DataValidator
from src.utils.data_generator import UrbanDataGenerator

__version__ = "1.0.0"
__author__ = "Urban Analytics Team"
__all__ = [
    'ETLPipeline',
    'ComparativeAnalysis',
    'AdvancedStatistics',
    'TimeSeriesAnalysis',
    'PredictiveModeling',
    'DataValidator',
    'UrbanDataGenerator',
    'setup_logging',
    'load_config'
]
