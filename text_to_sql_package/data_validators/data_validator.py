from typing import List, Protocol, Type, TypeVar
import pandas as pd

T = TypeVar('T')

class DataValidator(Protocol):
  
  """Interface for classes that handle data validation."""
  
  def validate(self, data: str, model_type: Type[T]) -> List[T]:
    """
    Validates data string based on provided model type.
    
    Parameters:
    data (str): Data to validate
    model_type (Type[T]): Type of model used to validate data

    Returns:
    List[T]: List of validated objects. Empty list if there is no valid data.
    """
    ...
    
  def create_model_from_df(self, df: pd.DataFrame) -> Type[T]:
    """
    Creates a data validation model based on provided dataframe.
    
    Parameters:
    df (pd.DataFrame): Dataframe to create the model from

    Returns:
    Type[T]: Data validation model
    """
    ...