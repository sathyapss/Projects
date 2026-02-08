import pandas as pd
import numpy as np
from scipy import stats

class EDA:
    def __init__(self, df):
        self.df = df
        
    def get_basic_stats(self):
        """Returns descriptive statistics."""
        return self.df.describe()

    def get_missing_values(self):
        """Returns count and percentage of missing values."""
        missing = self.df.isnull().sum()
        percent = (self.df.isnull().sum() / len(self.df)) * 100
        return pd.DataFrame({'Missing Count': missing, 'Percent': percent})

    def get_columns_by_type(self):
        """Separates numerical and categorical columns."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.df.select_dtypes(exclude=[np.number]).columns.tolist()
        return numeric_cols, categorical_cols
        
    def detect_outliers(self, threshold=3):
        """Detects outliers using Z-score for numerical columns."""
        numeric_cols, _ = self.get_columns_by_type()
        outliers_dict = {}
        for col in numeric_cols:
            z_scores = np.abs(stats.zscore(self.df[col].dropna()))
            outliers = self.df[col].dropna()[z_scores > threshold]
            if not outliers.empty:
                outliers_dict[col] = outliers.tolist()
        return outliers_dict

    def get_correlation_matrix(self):
        """Returns correlation matrix for numerical columns."""
        numeric_cols, _ = self.get_columns_by_type()
        if len(numeric_cols) > 1:
            return self.df[numeric_cols].corr()
        return None
