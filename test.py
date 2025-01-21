from data_loaders.data_loader import DataLoader 
from data_loaders.csv_loader import CSVLoader 
from data_loaders.tsv_loader import TSVLoader 
from data_loaders.excel_loader import ExcelLoader 
from llm_providers.litellm_provider import LiteLLMProvider 
from database_connectors.sqlite_connector import SQLiteDatabaseConnector 
from data_validators.pydantic_validator import PydanticValidator 
from text_to_sql import TextToSQL 
from utils.file_utils import save_json_to_file, replace_file_type_with_json
from dotenv import load_dotenv
import os
load_dotenv(override=True)

file_path = "sample_data/family.csv"
user_prompt = "Give me information on all female members of my family."

# # Pydantic warning
# import warnings
# warnings.filterwarnings("ignore", message="Valid config keys have changed in V2")

def create_data_loader(file_path: str) -> DataLoader:
  """
  Create data loader depending on specified file type.
  
  Parameters:
  file_path (str): File path for given dataset
  
  Returns:
  DataLoader: Depending on file type CSVLoader, TSVLoader or ExcelLoader
  """
  if file_path.lower().endswith('.csv'):
    return CSVLoader()
  elif file_path.lower().endswith('.tsv'):
    return TSVLoader()
  elif file_path.lower().endswith(('.xlsx', '.xls')):
    return ExcelLoader()
  else:
    raise ValueError(f"Specified file format not accepted. Only accepts .csv, .tsv, .xlsx and .xls")

if __name__ == "__main__":
   
  try:
    model_name = os.getenv('MODEL_NAME')
    print(f"Environment variables loaded. Model_name = {model_name}")
    
  except Exception as e:
    print(f"Error loading environment variables: {e}")
  
  try: 
    # Initialize the components 
    data_loader = create_data_loader(file_path=file_path)
    llm_provider = LiteLLMProvider(model_name=model_name)
    database_connector = SQLiteDatabaseConnector(db_path="test.db")
    data_validator = PydanticValidator()
    
  except Exception as e:
    print(f"Error initializing components: {e}") 
    
  try:
    # Create the main TextToSQL object
    text_to_sql = TextToSQL(data_loader=data_loader, llm_provider=llm_provider, database_connector=database_connector, data_validator=data_validator) 
    
  except Exception as e:
    print(f"Error initializing TextToSQL object: {e}") 
    
  try:
    # Run the query 
    result = text_to_sql.extract_data_from_file_with_prompt(file_path=file_path, user_prompt=user_prompt) 
    
    # Print the result 
    print("Result of query:")
    print(result)
    
    # Store to JSON file
    save_json_to_file(json_str=result, file_path=replace_file_type_with_json(file_path)) 
    
  except Exception as e:
    print(f"Error running query on LLM: {e}") 
  


  