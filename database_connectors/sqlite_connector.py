import sqlite3
from typing import List, Dict, Self
import pandas as pd
from database_connectors.sql_database_connector import SQLDatabaseConnector

class SQLiteDatabaseConnector:
  
  def __init__(self, db_path: str):
    """
    Class constructor.
    
    Parameters:
    db_path (str): Path to database
    """
    
    self.db_path = db_path
    self.connection = None
    
  def __enter__(self) -> Self:
    """
    Enter runtime context (connect to database).
    Reference: https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers
    
    Returns:
    Self: database object
    """

    self.connect_to_database()
    return self
    
  def __exit__(self, exc_type, exc_value, traceback) -> None:
    """
    Exit runtime context (close database connection).
    Reference: https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers
    """
    
    self.close_database()
    
  def connect_to_database(self) -> None:
    """Connect to the SQLite database."""
    
    print(f"Connecting to SQLite database: {self.db_path}...")
    
    try:
      self.connection = sqlite3.connect(self.db_path)
      print(f"Connected to SQLite database.")
      
    except sqlite3.Error as e:
      print(f"Error connecting to database: {e}")
      raise 
    
  def close_database(self) -> None:
    """Close connection to the SQLite database."""
    
    if self.connection:
      self.connection.close()
      print(f"Connection to SQLite database closed.")
    
  def execute_sql_query(self, query: str) -> List[Dict]:
    """
    Run SQL query on the SQLite database and return result as a list of dictionaries.
    
    Parameters:
    query (str): SQL query to be executed.

    Returns:
    List[Dict]: Result of the SQL query
    """
    
    print(f"Executing SQL query on SQLite database...")
    
    if not query:
      print(f"SQL query is empty.")
      raise
    
    results = []
    
    try:

      with self.connection as conn:
    
        # Run SQL query
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Get result
        cols = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        # Convert result to list of dictionaries
        for row in rows:
          results.append({cols[i]: row[i] for i in range(len(cols))})
          
        print("SQL query executed.")
        print(f"Results: {results}")
    
    except sqlite3.Error as e:
      print(f"Error executing SQL query: {query}")
      raise
      
    return results
  
  def create_table_from_df(self, df: pd.DataFrame, table_name: str) -> None:
    """
    Create a SQL table from a Pandas dataframe.

    Parameters:
    df (pd.DataFrame): Pandas dataframe to create table
    table_name (str): Name of SQL table
    """
    
    print(f"Creating table {table_name} from dataframe...")

    try:
      # Create SQL table
      with self.connection as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Table {table_name} created.")
      
    except Exception as e:
      print(f"Error creating table {table_name}: {e}")
      raise
    
    
    
    
    