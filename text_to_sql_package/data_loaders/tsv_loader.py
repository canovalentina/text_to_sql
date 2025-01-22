import pandas as pd
from text_to_sql_package.utils.dataframe_utils import clean_dataframe 
from text_to_sql_package.utils.file_utils import check_file_exists, check_file_type
from text_to_sql_package.data_loaders.data_loader import DataLoader

class TSVLoader:
  
  def load_data(self, file_path: str) -> pd.DataFrame:
    """
    Loads data from the specified TSV file path into a Pandas dataframe.
    
    Parameters:
    file_path (str): File path to given dataset (.tsv file)

    Returns:
    pd.DataFrame: Content of dataset in a Pandas dataframe
    """
    
    print(f"Loading TSV file: {file_path}...")
    
    # Check if the file exists 
    check_file_exists(file_path=file_path)
    
    # Check if the file path ends with '.tsv' 
    check_file_type(file_path=file_path, file_types=['.tsv'])
    
    try:
      # Read TSV file
      df = pd.read_csv(file_path, sep='\t')
      
    except Exception as e:
      print(f"Error reading TSV file from Pandas dataframe: {e}")
      raise
    
    # Dataframe cleanup
    df = clean_dataframe(df)
    
    print("TSV file loaded onto dataframe and cleaned.")
    
    return df