import pandas as pd
import json
from data_loaders.data_loader import DataLoader
from llm_providers.llm_provider import LLMProvider
from database_connectors.sql_database_connector import SQLDatabaseConnector
from data_validators.data_validator import DataValidator
from utils.dataframe_utils import generate_schema_from_dataframe

class TextToSQL:
  
  """Class in charge of bringing together the different interfaces of this package to be able to connect to a SQL database, generate a SQL query from a natural language prompt using an LLM, extract data from the database, validate the output, and return it in JSON format.
  """
  
  def __init__(self, data_loader: DataLoader, llm_provider: LLMProvider, database_connector: SQLDatabaseConnector, data_validator: DataValidator):
    
    """Class constructor.
    
    Parameters:
    data_loader (DataLoader): Object that implements the DataLoader interface, in charge of loading the data from an input file.
    llm_provider (LLMProvider): Object that implement the LLMProvider interface, in charge of providing and prompting an LLM.
    database_connector (SQLDatabaseConnector): Object that implements the SQLDatabaseConnector interface, in charge of connecting to a SQL database.
    data_validator (DataValidator): Object that implements the DataValidator interface, in charge of validating the output data.
    """
    
    self.data_loader = data_loader
    self.llm_provider = llm_provider
    self.database_connector = database_connector
    self.data_validator = data_validator
    
  def extract_data_from_file_with_prompt(self, file_path: str, user_prompt: str) -> str:
    """
    Main entry point for the package. From any given dataset, allow for user to prompt with natural language, and extract rows in the form of list of validated JSONs.

    Parameters:
    file_path (str): File path for given dataset
    user_prompt (str): Natural language prompt from the user that will be used to generate query
    
    Returns:
    str: JSON string with extracted data
    """ 
 
    try:
      df = self.load_and_prepare_data(file_path=file_path)
      schema = self.create_table_and_schema(df=df)
      results = self.generate_and_execute_sql_query(user_prompt=user_prompt, schema=schema)
      json_str = self.validate_and_format_results(df=df, results=results)
      return json_str
          
    except Exception as e:
      print(f"Error extracting data: {e}")
      empty_json_str = "[]"
      return empty_json_str
    
  ### Functions below are all helper functions for extract_data_from_file_with_prompt().
    
  def load_and_prepare_data(self, file_path: str) -> pd.DataFrame:
    """
    Loads and cleans data from provided file path using the DataLoader, converting it to a Pandas dataframe.
    
    Parameters:
    file_path (str): File path for given dataset
    
    Returns:
    pd.DataFrame: Content of dataset in a Pandas dataframe    
    """
        
    try:
      # Load data from the provided file pathusing a DataLoader
      df = self.data_loader.load_data(file_path)
      return df
      
    except Exception as e:
      print(f"Error loading data with DataLoader: {e}")
      raise
    
  def create_table_and_schema(self, df: pd.DataFrame) -> str:
    """
    Creates a temporary SQL table using the SQLDatabaseConnector and the schema of the table in a string
    
    Parameters:
    df (pd.DataFrame): Pandas dataframe to create table
    
    Returns:
    str: Schema of the table  
    """
    
    try:
      with self.database_connector as db:
      
        # Create a temporary table for the dataframe
        table_name = "text_to_sql_temp"
        db.create_table_from_df(df=df, table_name=table_name)
        
        # Generate a schema for the table
        schema = generate_schema_from_dataframe(df=df, table_name=table_name)
        
        return schema
      
    except Exception as e:
      print(f"Error creating table and generating schema with SQLDatabaseConnector: {e}")
      raise
    
  def generate_and_execute_sql_query(self, user_prompt: str, schema: str):
    """
    Generates the SQL query using the LLMProvider.
    Then, runs SQL query using the SQLDatabaseConnector and return result as a list of dictionaries.
    
    Parameters:
    user_prompt (str): Natural language prompt to query the dataset.
    schema (str): Table schema for the SQL query

    Returns:
    List[Dict]: Result of the SQL query
    """
    try:
      # Send the prompt and schema to the LLM using the LLMProvider to generate the SQL query
      query = self.llm_provider.generate_sql_query(user_prompt=user_prompt, schema=schema)
      
      with self.database_connector as db:
      
        # Query the database
        results = db.execute_sql_query(query)
        
        return results

    except Exception as e:
      print(f"Error generating or executing query: {e}")
      raise
  
  def validate_and_format_results(self, df: pd.DataFrame, results: list) -> str:
    """
    Create a data validation model based on provided dataframe using the DataValidator.
    Then, validates data based on provided model type.
    
    Parameters:
    df (pd.DataFrame): Dataframe to create the Pydantic model from
    results (list): List with output from the SQL query

    Returns:
    str: JSON string with extracted data
    """
    try:
      # Create Pydantic model to validate results
      pydantic_model = self.data_validator.create_model_from_df(df)
      validated_results = self.data_validator.validate(json.dumps(results), pydantic_model)
    
      # Convert validated output to a JSON string
      json_result = [result.model_dump() for result in validated_results]
      json_str = json.dumps(json_result)
      return json_str
    
    except Exception as e:
      print(f"Error validating results: {e}")
      raise