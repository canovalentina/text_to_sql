import pandas as pd
from text_to_sql_package.utils.dataframe_utils import clean_dataframe 
from text_to_sql_package.utils.file_utils import check_file_exists, check_file_type
from text_to_sql_package.data_loaders.data_loader import DataLoader

class ExcelLoader:
    
  def load_data(self, file_path: str) -> pd.DataFrame:
    """
    Loads data from the specified Excel file path into a Pandas dataframe.
    
    Parameters:
    file_path (str): File path to given dataset (.xls or .xlsx file)

    Returns:
    pd.DataFrame: Content of dataset in a Pandas dataframe
    """
    
    print(f"Loading Excel file: {file_path}...")
    
    # Check if the file exists 
    check_file_exists(file_path=file_path)
    
    # Check if the file path ends with  '.xls' or '.xlsx'
    check_file_type(file_path=file_path, file_types=['.xls', '.xlsx'])
    
    try:
      # Read Excel file
      df = pd.read_excel(file_path)
      
    except Exception as e:
      print(f"Error reading Excel file from Pandas dataframe: {e}")
      raise
    
    # Dataframe cleanup
    df = clean_dataframe(df)
    
    print("Excel file loaded onto dataframe and cleaned.")
    
    #Return dataframe
    return df