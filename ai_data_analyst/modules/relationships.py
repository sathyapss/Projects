import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

class RelationshipManager:
    def __init__(self, df):
        self.df = df

    def get_correlation_matrix(self):
        """Calculates correlation matrix for numerical columns."""
        numeric_df = self.df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            return numeric_df.corr()
        return None

    def plot_correlation_heatmap(self):
        """Generates a heatmap for correlations."""
        corr = self.get_correlation_matrix()
        if corr is not None:
            fig = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Heatmap")
            return fig
        return None

    def find_highly_correlated_pairs(self, threshold=0.8):
        """Identifies variable pairs with correlation above threshold."""
        corr = self.get_correlation_matrix()
        if corr is None:
            return []
        
        pairs = []
        columns = corr.columns
        for i in range(len(columns)):
            for j in range(i+1, len(columns)):
                if abs(corr.iloc[i, j]) >= threshold:
                    pairs.append((columns[i], columns[j], corr.iloc[i, j]))
        return pairs

    def detect_trends(self, date_col, value_col):
        """Simple trend analysis over a time column."""
        try:
            temp_df = self.df.copy()
            temp_df[date_col] = pd.to_datetime(temp_df[date_col])
            temp_df = temp_df.sort_values(by=date_col)
            
            # Resample? For now just line plot
            fig = px.line(temp_df, x=date_col, y=value_col, title=f"Trend of {value_col} over {date_col}")
            
            # Calculate simple growth rate
            start_val = temp_df[value_col].iloc[0]
            end_val = temp_df[value_col].iloc[-1]
            growth = ((end_val - start_val) / start_val) * 100 if start_val != 0 else 0
            
            return fig, growth
        except Exception as e:
            return None, str(e)

    def identify_potential_causes(self, target_col):
        """
        Uses correlation to suggest potential drivers for a target variable.
        (Simplified 'Causation' for MVP)
        """
        corr = self.get_correlation_matrix()
        if corr is None or target_col not in corr.columns:
            return []
        
        # Sort by absolute correlation to target
        correlations = corr[target_col].drop(target_col) # Remove target itself
        sorted_corr = correlations.abs().sort_values(ascending=False)
        
        return sorted_corr.head(5).to_dict()
