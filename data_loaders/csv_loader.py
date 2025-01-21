import pandas as pd
from utils.dataframe_utils import clean_dataframe 
from utils.file_utils import check_file_exists, check_file_type
from data_loaders.data_loader import DataLoader

class CSVLoader:
  
  def load_data(self, file_path: str) -> pd.DataFrame:
    """
    Loads data from the specified CSV file path into a Pandas dataframe.
    
    Parameters:
    file_path (str): File path to given dataset (.csv file)

    Returns:
    pd.DataFrame: Content of dataset in a Pandas dataframe
    """
    
    print(f"Loading CSV file: {file_path}...")

    # Check if the file exists 
    check_file_exists(file_path=file_path)
    
    # Check if the file path ends with '.csv' 
    check_file_type(file_path=file_path, file_types=['.csv'])
    
    try:
      # Read CSV file
      df = pd.read_csv(file_path)
      
    except Exception as e:
      print(f"Error reading CSV file from Pandas dataframe: {e}")
      raise
      
    # Dataframe cleanup
    df = clean_dataframe(df)
    
    print("CSV file loaded onto dataframe and cleaned.")
    
    return df