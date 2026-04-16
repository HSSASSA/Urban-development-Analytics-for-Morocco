"""
Synthetic data generation for urban development analytics
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple

class UrbanDataGenerator:
    """Generate realistic synthetic data for Moroccan urban development"""
    
    REGIONS = [
        "Casablanca-Settat", "Fès-Meknès", "Marrakech-Safi",
        "Rabat-Salé-Kénitra", "Tanger-Tétouan-Al Hoceïma"
    ]
    
    CITY_TYPES = ["Metropolitan", "Urban", "Peri-urban", "Rural"]
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
    
    @staticmethod
    def generate_urban_indicators(n_records: int = 5000) -> pd.DataFrame:
        """Generate urban indicator data"""
        np.random.seed(42)
        
        data = {
            'indicator_id': range(1, n_records + 1),
            'region': np.random.choice(UrbanDataGenerator.REGIONS, n_records),
            'city': [f"City_{i}" for i in range(1, n_records + 1)],
            'city_type': np.random.choice(UrbanDataGenerator.CITY_TYPES, n_records),
            'year': np.random.randint(2015, 2024, n_records),
            'population': np.random.gamma(2, 2) * 100000 + 10000,
            'urban_area_km2': np.random.gamma(1.5, 1) * 200 + 50,
            'population_density': np.random.gamma(2, 0.5) * 500 + 100,
            'housing_units': np.random.gamma(2, 1.5) * 10000 + 2000,
            'houses_with_water_access': np.random.uniform(0.7, 0.99, n_records),
            'houses_with_electricity': np.random.uniform(0.85, 1.0, n_records),
            'unemployment_rate': np.random.uniform(0.08, 0.25, n_records),
            'gdp_per_capita': np.random.normal(35000, 15000, n_records),
        }
        
        df = pd.DataFrame(data)
        
        # Add correlations
        df['houses_with_water_access'] = np.clip(
            df['gdp_per_capita'] / df['gdp_per_capita'].max() * 0.95 + 
            np.random.normal(0, 0.05, n_records), 0.6, 1.0
        )
        df['houses_with_electricity'] = np.clip(
            df['houses_with_water_access'] + np.random.normal(0, 0.02, n_records), 0.75, 1.0
        )
        df['unemployment_rate'] = np.clip(
            0.20 - (df['gdp_per_capita'] / df['gdp_per_capita'].max() * 0.12) + 
            np.random.normal(0, 0.02, n_records), 0.05, 0.30
        )
        
        return df
    
    @staticmethod
    def generate_housing_data(n_records: int = 3000) -> pd.DataFrame:
        """Generate housing and real estate data"""
        np.random.seed(42)
        
        data = {
            'housing_id': range(1, n_records + 1),
            'region': np.random.choice(UrbanDataGenerator.REGIONS, n_records),
            'city': [f"City_{i % 50}" for i in range(1, n_records + 1)],
            'year': np.random.randint(2015, 2024, n_records),
            'housing_units_completed': np.random.gamma(2, 200),
            'housing_units_planned': np.random.gamma(2, 300),
            'affordable_housing_units': np.random.gamma(2, 150),
            'price_per_sqm_dirham': np.random.gamma(2, 3000) + 5000,
            'vacancy_rate': np.random.uniform(0.05, 0.20, n_records),
            'household_size': np.random.normal(4.5, 0.8, n_records),
        }
        
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_infrastructure_data(n_records: int = 2000) -> pd.DataFrame:
        """Generate infrastructure and public services data"""
        np.random.seed(42)
        
        services = ["Roads", "Water System", "Electricity Grid", "Healthcare", "Education"]
        
        data = {
            'infrastructure_id': range(1, n_records + 1),
            'region': np.random.choice(UrbanDataGenerator.REGIONS, n_records),
            'service_type': np.random.choice(services, n_records),
            'year': np.random.randint(2015, 2024, n_records),
            'investment_millions_dh': np.random.gamma(1.5, 50),
            'coverage_rate': np.random.uniform(0.6, 1.0, n_records),
            'maintenance_status': np.random.choice(["Good", "Fair", "Poor"], n_records),
            'projects_completed': np.random.poisson(3, n_records),
            'projects_ongoing': np.random.poisson(2, n_records),
        }
        
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_migration_data(n_records: int = 2500) -> pd.DataFrame:
        """Generate internal migration and urbanization data"""
        np.random.seed(42)
        
        data = {
            'migration_id': range(1, n_records + 1),
            'origin_region': np.random.choice(UrbanDataGenerator.REGIONS, n_records),
            'destination_region': np.random.choice(UrbanDataGenerator.REGIONS, n_records),
            'year': np.random.randint(2015, 2024, n_records),
            'migrants_count': np.random.gamma(2, 100) + 50,
            'rural_to_urban_ratio': np.random.uniform(0.3, 0.9, n_records),
            'urban_to_urban_ratio': np.random.uniform(0.1, 0.7, n_records),
        }
        
        df = pd.DataFrame(data)
        # Ensure ratios sum to approximately 1
        df['other_migration_ratio'] = 1 - (df['rural_to_urban_ratio'] + df['urban_to_urban_ratio'])
        
        return df
    
    @staticmethod
    def generate_all_datasets() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Generate all datasets at once"""
        urban = UrbanDataGenerator.generate_urban_indicators()
        housing = UrbanDataGenerator.generate_housing_data()
        infrastructure = UrbanDataGenerator.generate_infrastructure_data()
        migration = UrbanDataGenerator.generate_migration_data()
        
        return urban, housing, infrastructure, migration
