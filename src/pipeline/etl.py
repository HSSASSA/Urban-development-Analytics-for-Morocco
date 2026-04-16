"""
ETL Pipeline - Extract, Transform, Load operations
"""
import pandas as pd
import sqlite3
from pathlib import Path
from typing import Optional, List
import logging
from src.utils.validators import DataValidator
from src.utils.data_generator import UrbanDataGenerator

class ETLPipeline:
    """End-to-end ETL pipeline for urban development data"""
    
    def __init__(self, db_path: str = "./data/warehouse/urban_analytics.db", logger=None):
        self.db_path = db_path
        self.logger = logger or logging.getLogger(__name__)
        self.validator = DataValidator(logger=self.logger)
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def extract_data(self, source: str = 'generate') -> dict:
        """
        Extract data from source (synthetic, CSV, API, etc.)
        
        Args:
            source: 'generate' for synthetic data, or path to CSV file
        
        Returns:
            Dictionary of dataframes
        """
        self.logger.info(f"Extracting data from source: {source}")
        
        if source == 'generate':
            urban, housing, infrastructure, migration = UrbanDataGenerator.generate_all_datasets()
            return {
                'urban_indicators': urban,
                'housing': housing,
                'infrastructure': infrastructure,
                'migration': migration
            }
        else:
            # Load from CSV files
            data = {}
            for file in Path(source).glob('*.csv'):
                data[file.stem] = pd.read_csv(file)
                self.logger.info(f"Loaded {file.stem}: {len(data[file.stem])} rows")
            
            return data
    
    def transform_urban_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform urban indicators data"""
        self.logger.info("Transforming urban indicators...")
        
        # Data type conversions
        df = df.copy()
        df['year'] = df['year'].astype('int32')
        df['population'] = df['population'].astype('int32')
        df['housing_units'] = df['housing_units'].astype('int32')
        df['population_density'] = df['population_density'].round(2)
        df['unemployment_rate'] = (df['unemployment_rate'] * 100).round(2)  # Convert to percentage
        df['gdp_per_capita'] = df['gdp_per_capita'].round(2)
        
        # Create derived metrics
        df['urbanization_rate'] = (df['population'] / (df['population'] + 1000)).round(3)
        df['housing_need_index'] = (df['population'] / (df['housing_units'] + 1)).round(2)
        df['infrastructure_score'] = (
            df['houses_with_water_access'] + df['houses_with_electricity']
        ) / 2
        
        # Missing value imputation
        df['unemployment_rate'].fillna(df['unemployment_rate'].median(), inplace=True)
        
        self.logger.info(f"Urban indicators transformed: {df.shape}")
        return df
    
    def transform_housing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform housing data"""
        self.logger.info("Transforming housing data...")
        
        df = df.copy()
        df['year'] = df['year'].astype('int32')
        df['housing_units_completed'] = df['housing_units_completed'].astype('int32')
        df['housing_units_planned'] = df['housing_units_planned'].astype('int32')
        df['affordable_housing_units'] = df['affordable_housing_units'].astype('int32')
        df['price_per_sqm_dirham'] = df['price_per_sqm_dirham'].round(2)
        df['vacancy_rate'] = (df['vacancy_rate'] * 100).round(2)
        df['household_size'] = df['household_size'].round(1)
        
        # Derived metrics
        df['housing_completion_rate'] = (
            df['housing_units_completed'] / (df['housing_units_planned'] + 1)
        ).round(3)
        df['affordable_housing_ratio'] = (
            df['affordable_housing_units'] / (df['housing_units_completed'] + 1)
        ).round(3)
        df['affordability_index'] = (
            df['price_per_sqm_dirham'] / df['price_per_sqm_dirham'].median()
        ).round(2)
        
        self.logger.info(f"Housing data transformed: {df.shape}")
        return df
    
    def transform_infrastructure(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform infrastructure data"""
        self.logger.info("Transforming infrastructure data...")
        
        df = df.copy()
        df['year'] = df['year'].astype('int32')
        df['investment_millions_dh'] = df['investment_millions_dh'].round(2)
        df['coverage_rate'] = (df['coverage_rate'] * 100).round(2)
        df['projects_completed'] = df['projects_completed'].astype('int32')
        df['projects_ongoing'] = df['projects_ongoing'].astype('int32')
        
        # Status mapping
        status_map = {"Good": 3, "Fair": 2, "Poor": 1}
        df['maintenance_score'] = df['maintenance_status'].map(status_map)
        
        # Derived metrics
        df['total_projects'] = df['projects_completed'] + df['projects_ongoing']
        df['completion_efficiency'] = (
            df['projects_completed'] / (df['total_projects'] + 1)
        ).round(3)
        
        self.logger.info(f"Infrastructure data transformed: {df.shape}")
        return df
    
    def transform_migration(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform migration data"""
        self.logger.info("Transforming migration data...")
        
        df = df.copy()
        df['year'] = df['year'].astype('int32')
        df['migrants_count'] = df['migrants_count'].astype('int32')
        
        # Normalize migration ratios
        df['rural_to_urban_ratio'] = (df['rural_to_urban_ratio'] * 100).round(2)
        df['urban_to_urban_ratio'] = (df['urban_to_urban_ratio'] * 100).round(2)
        df['other_migration_ratio'] = (df['other_migration_ratio'] * 100).round(2)
        
        # Urbanization metric
        df['urbanization_intensity'] = df['rural_to_urban_ratio'] / 100
        
        self.logger.info(f"Migration data transformed: {df.shape}")
        return df
    
    def load_to_database(self, dataframes: dict) -> None:
        """Load transformed data to SQLite database"""
        self.logger.info(f"Loading data to database: {self.db_path}")
        
        try:
            connection = sqlite3.connect(self.db_path)
            
            for table_name, df in dataframes.items():
                df.to_sql(table_name, connection, if_exists='replace', index=False)
                self.logger.info(f"Loaded {table_name}: {len(df)} rows")
            
            # Create indexes for performance
            cursor = connection.cursor()
            cursor.execute("CREATE INDEX idx_urban_region_year ON urban_indicators(region, year)")
            cursor.execute("CREATE INDEX idx_housing_region_year ON housing(region, year)")
            cursor.execute("CREATE INDEX idx_infrastructure_service ON infrastructure(service_type)")
            cursor.execute("CREATE INDEX idx_migration_origin_dest ON migration(origin_region, destination_region)")
            connection.commit()
            
            self.logger.info("Indexes created successfully")
            connection.close()
            
        except Exception as e:
            self.logger.error(f"Error loading data to database: {str(e)}")
            raise
    
    def run_pipeline(self, source: str = 'generate', save_processed: bool = True) -> dict:
        """Run complete ETL pipeline"""
        self.logger.info("=" * 60)
        self.logger.info("Starting ETL Pipeline")
        self.logger.info("=" * 60)
        
        # Extract
        raw_data = self.extract_data(source)
        
        # Transform
        transformed_data = {
            'urban_indicators': self.transform_urban_indicators(raw_data['urban_indicators']),
            'housing': self.transform_housing(raw_data['housing']),
            'infrastructure': self.transform_infrastructure(raw_data['infrastructure']),
            'migration': self.transform_migration(raw_data['migration']),
        }
        
        # Validate
        for table_name, df in transformed_data.items():
            self.logger.info(f"Validating {table_name}...")
            valid, errors = self.validator.validate_schema(df, {})
            outliers = self.validator.detect_outliers(
                df, 
                df.select_dtypes(include=['float64', 'int32', 'int64']).columns.tolist()
            )
        
        # Load
        self.load_to_database(transformed_data)
        
        # Save processed data as CSV
        if save_processed:
            processed_path = Path("./data/processed")
            processed_path.mkdir(parents=True, exist_ok=True)
            for table_name, df in transformed_data.items():
                df.to_csv(processed_path / f"{table_name}.csv", index=False)
                self.logger.info(f"Saved {table_name}.csv")
        
        self.logger.info("=" * 60)
        self.logger.info("ETL Pipeline completed successfully!")
        self.logger.info("=" * 60)
        
        return transformed_data
