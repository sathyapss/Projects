import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, inspect

class DataConnector:
    def __init__(self):
        self.engine = None
        self.metadata = None

    def load_csv(self, file_object):
        """Loads a CSV or Excel file into a Pandas DataFrame."""
        try:
            if file_object.name.endswith('.csv'):
                encodings = ['utf-8', 'cp1252', 'latin1', 'ISO-8859-1']
                last_error = None
                
                for encoding in encodings:
                    try:
                        file_object.seek(0)
                        return pd.read_csv(file_object, encoding=encoding)
                    except Exception as e:
                        last_error = e
                        continue
                
                return f"Failed to decode CSV. Last error: {str(last_error)}"
                
            elif file_object.name.endswith(('.xls', '.xlsx')):
                return pd.read_excel(file_object)
            else:
                return None
        except Exception as e:
            return str(e)

    def connect_db(self, db_type, host, port, user, password, db_name):
        """Establishes a database connection."""
        try:
            if db_type == "PostgreSQL":
                url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
            elif db_type == "MySQL":
                url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
            elif db_type == "SQLite":
                url = f"sqlite:///{db_name}" # db_name is path for sqlite
            else:
                return "Unsupported Database Type"

            self.engine = create_engine(url)
            self.metadata = inspect(self.engine)
            return True
        except Exception as e:
            return str(e)

    def get_tables(self):
        """Returns a list of tables in the connected database."""
        if self.metadata:
            return self.metadata.get_table_names()
        return []

    def get_table_data(self, table_name, start_row, limit=1000):
        """Fetches data from a specific table."""
        if self.engine:
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            return pd.read_sql(query, self.engine)
        return None
    
    def execute_query(self, query):
        """Executes a custom SQL query."""
        if self.engine:
            try:
                return pd.read_sql(query, self.engine)
            except Exception as e:
                return str(e)
        return None
