import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple


class CSVDataAnalyzer:
    """Analyzer for CSV data that provides insights and statistics."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the analyzer with a DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame to analyze
        """
        self.df = df
        self.numeric_columns = self._get_numeric_columns()
        self.categorical_columns = self._get_categorical_columns()
    
    def _get_numeric_columns(self) -> List[str]:
        """Get list of numeric columns in the DataFrame."""
        return list(self.df.select_dtypes(include=[np.number]).columns)
    
    def _get_categorical_columns(self) -> List[str]:
        """Get list of categorical columns in the DataFrame."""
        # Filter out columns that contain lists or other non-hashable types
        categorical_cols = []
        for col in self.df.select_dtypes(include=['object']).columns:
            # Check if the column contains hashable values
            try:
                # Test with a small sample of values
                sample_values = self.df[col].dropna().head(5)
                for val in sample_values:
                    if pd.notna(val):
                        # Try to hash the value to check if it's hashable
                        hash(val)
                categorical_cols.append(col)
            except (TypeError, ValueError):
                # Skip columns with unhashable types like lists or other complex objects
                continue
        return categorical_cols
    
    def get_basic_info(self) -> Dict[str, Any]:
        """
        Get basic information about the dataset.
        
        Returns:
            dict: Basic information including shape, columns, etc.
        """
        info = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'numeric_columns': self.numeric_columns,
            'categorical_columns': self.categorical_columns,
            'memory_usage': self.df.memory_usage(deep=True).sum()
        }
        return info
    
    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Get summary statistics for numeric columns.
        
        Returns:
            pd.DataFrame: Summary statistics
        """
        if len(self.numeric_columns) > 0:
            return self.df[self.numeric_columns].describe()
        else:
            return pd.DataFrame()
    
    def get_categorical_summary(self) -> Dict[str, Any]:
        """
        Get summary for categorical columns.
        
        Returns:
            dict: Summary of categorical columns
        """
        summary = {}
        for col in self.categorical_columns:
            try:
                summary[col] = {
                    'unique_values': self.df[col].nunique(),
                    'top_values': self.df[col].value_counts().head(5).to_dict()
                }
            except Exception:
                # Handle case where value_counts fails
                summary[col] = {
                    'unique_values': 'Unable to compute',
                    'top_values': 'Unable to compute'
                }
        return summary
    
    def get_missing_data_info(self) -> pd.DataFrame:
        """
        Get information about missing data.
        
        Returns:
            pd.DataFrame: Missing data information
        """
        missing_data = self.df.isnull().sum()
        missing_percent = 100 * missing_data / len(self.df)
        
        missing_df = pd.DataFrame({
            'missing_count': missing_data,
            'missing_percent': missing_percent
        })
        
        return missing_df[missing_df['missing_count'] > 0]
    
    def get_correlation_matrix(self) -> pd.DataFrame:
        """
        Get correlation matrix for numeric columns.
        
        Returns:
            pd.DataFrame: Correlation matrix
        """
        if len(self.numeric_columns) > 1:
            return self.df[self.numeric_columns].corr()
        else:
            return pd.DataFrame()
    
    def get_column_types(self) -> Dict[str, str]:
        """
        Get data types of all columns.
        
        Returns:
            dict: Column names and their data types
        """
        return self.df.dtypes.astype(str).to_dict()
    
    def get_data_sample(self, n: int = 5) -> pd.DataFrame:
        """
        Get a sample of the data.
        
        Args:
            n (int): Number of rows to sample
            
        Returns:
            pd.DataFrame: Sample of the data
        """
        return self.df.head(n)