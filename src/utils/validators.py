"""
Data validation and quality checks utilities
"""
import pandas as pd
import numpy as np
from typing import Tuple, List, Dict
from datetime import datetime

class DataValidator:
    """Comprehensive data validation framework"""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.validation_report = {}
    
    def validate_schema(self, df: pd.DataFrame, expected_schema: Dict) -> Tuple[bool, List[str]]:
        """Validate dataframe schema against expected schema"""
        errors = []
        
        for col, expected_type in expected_schema.items():
            if col not in df.columns:
                errors.append(f"Missing column: {col}")
            elif not df[col].dtype == expected_type:
                errors.append(f"Column {col}: expected {expected_type}, got {df[col].dtype}")
        
        return len(errors) == 0, errors
    
    def check_nulls(self, df: pd.DataFrame, max_null_pct: float = 0.5) -> Tuple[bool, Dict]:
        """Check for null values and their proportion"""
        null_report = {}
        for col in df.columns:
            null_pct = df[col].isnull().sum() / len(df)
            null_report[col] = null_pct
            
            if null_pct > max_null_pct:
                self.logger.warning(f"Column {col} has {null_pct*100:.2f}% null values")
        
        return True, null_report
    
    def check_duplicates(self, df: pd.DataFrame, subset: List[str] = None) -> Tuple[bool, int]:
        """Check for duplicate rows"""
        if subset:
            duplicates = df.duplicated(subset=subset).sum()
        else:
            duplicates = df.duplicated().sum()
        
        if duplicates > 0:
            self.logger.warning(f"Found {duplicates} duplicate rows")
        
        return duplicates == 0, duplicates
    
    def detect_outliers(self, df: pd.DataFrame, numeric_cols: List[str], 
                       method: str = 'iqr', threshold: float = 3.0) -> Dict[str, int]:
        """Detect outliers using IQR or Z-score method"""
        outliers = {}
        
        for col in numeric_cols:
            if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
                continue
            
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outlier_mask = (df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)
            else:  # z-score
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outlier_mask = z_scores > threshold
            
            outlier_count = outlier_mask.sum()
            outliers[col] = outlier_count
            
            if outlier_count > 0:
                self.logger.info(f"Column {col}: detected {outlier_count} outliers")
        
        return outliers
    
    def check_referential_integrity(self, df: pd.DataFrame, 
                                   foreign_keys: Dict[str, tuple]) -> Tuple[bool, List[str]]:
        """Check referential integrity (assumes dimension tables are loaded)"""
        errors = []
        
        for col, (ref_table, ref_col) in foreign_keys.items():
            # This is a placeholder - would need actual reference data
            self.logger.debug(f"Checking referential integrity for {col} -> {ref_table}.{ref_col}")
        
        return True, errors
    
    def generate_report(self) -> Dict:
        """Generate validation report"""
        return self.validation_report
