from typing import Protocol, List, Dict
import pandas as pd

class SQLDatabaseConnector(Protocol):
  
  """Interface for classes that handle the connection to a SQL database."""
  
  def connect_to_database(self) -> None:
    """Connect to the SQL database."""
    ...
    
  def close_database(self) -> None:
    """Close connection to the SQL database."""
    ...
  
  def execute_sql_query(self, query: str) -> List[Dict]:
    """
    Run SQL query on the database and return result as a list of dictionaries.
    
    Parameters:
    query (str): SQL query to be executed.

    Returns:
    List[Dict]: Result of the SQL query
    """
    ...
    
  def create_table_from_df(self, df: pd.DataFrame, table_name: str) -> None:
    """
    Create a SQL table from a Pandas dataframe.

    Parameters:
    df (pd.DataFrame): Pandas dataframe to create table
    table_name (str): Name of SQL table
    """
    ...