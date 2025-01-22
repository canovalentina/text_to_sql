import pandas as pd
from typing import Protocol

class DataLoader(Protocol):
  
  """Interface for classes that handle data load operations."""
  
  def load_data(self, file_path: str) -> pd.DataFrame:
    """
    Loads data from the specified file path into a Pandas dataframe.
    
    Parameters:
    file_path (str): File path to given dataset (Excel/csv/tsv file)

    Returns:
    pd.DataFrame: Content of dataset in a Pandas dataframe
    """
    ...