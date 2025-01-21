from typing import List, Type, Optional
import pandas as pd
import json
from pydantic import BaseModel, ValidationError, create_model
from datetime import datetime
from data_validators.data_validator import DataValidator

class PydanticValidator:
  
  def validate(self, data: str, model_type: Type[BaseModel]) -> List[BaseModel]:
    """
    Validates data string based on provided model type.
    
    Parameters:
    data (str): Data to validate
    model_type (Type[BaseModel]): Type of model used to validate data

    Returns:
    List[BaseModel]: List of validated objects. Empty list if there is no valid data.
    """
    
    print("Starting data validation with Pydantic library...")
    
    try:
      # Parse valid JSON string and convert to Python object
      json_data = json.loads(data)
      
      
      # Make sure data is list of dictionaries
      json_data_list = []
      
      # If only one JSON object
      if isinstance(json_data_list, dict):
        json_data_list = [json_data]
      # If already a list
      elif isinstance(json_data_list, list):
        json_data_list = json_data
      else:
        print(f"Error JSON not ready for validation: {e}")
        return []
        
      print(f"JSON ready for data validation")
      
    except json.JSONDecodeError as e:
      #If doesn't work, return empty list
      print(f"Error decoding JSON for data validation: {e}")
      return []
    
    # Create a list with the validatesd data
    validated_data = []
    
    for item in json_data_list:
      try:
        # Validate item and if validated, add to list
        validated_item = model_type.model_validate(item)
        validated_data.append(validated_item)
        
      except ValidationError as e:
        #Skip item if not validated
        print(f"Error validating {item}: {e}")
        continue
      
    # Return list with all validated data
    print(f"Data validation with Pydantic completed.")
    return validated_data
  
  def create_model_from_df(self, df: pd.DataFrame) -> Type[BaseModel]:
    """
    Creates a Pydantic model based on provided dataframe.
    
    Parameters:
    df (pd.DataFrame): Dataframe to create the model from

    Returns:
    Type[BaseModel]: Pydantic model
    """
        
    print("Creating Pydantic model with dataframe...")
    
    #Create a dict to store field definitions for Pydantic model
    fields = {}
    
    for col in df.columns:
      dtype_str = df[col].dtype.name
      
      # Map dtype and column name to Pydantic model
      # Note: Using startswith because Pandas can have int32, int64, datetime64[ns], etc.  
      if dtype_str.startswith('int'):
        fields[col] = (Optional[int], None)
      elif dtype_str.startswith('float'):
        fields[col] = (Optional[float], None)
      elif dtype_str.startswith('bool'):
        fields[col] = (Optional[bool], None)
      elif dtype_str.startswith(('datetime', 'date')):
        fields[col] = (Optional[datetime], None)
      else:
        fields[col] = (Optional[str], None)
      
    # Create model with mapped fields and return
    model = create_model('DynamicModel', **fields)
    
    print("Pydantic model created.")
    return model