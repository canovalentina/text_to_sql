import pandas as pd
import re

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
  """
  Basic data cleaning for a Pandas dataframe.
  
  Parameters: 
  df (pd.DataFrame): Pandas dataframe to clean
  
  Returns: 
  pd.DataFrame: Clean dataframe
  """

  try:
    # Remove special characaters from column names, and substitutes spaces for _
    df.columns = [re.sub(r'[^A-Z0-9_]+', '_', col, flags=re.IGNORECASE).strip('_') for col in df.columns]
    
    # Set column names to lowercase
    df.columns = df.columns.str.lower()
    print(f"Dataframe new column names: {list(df.columns)}")
    
  except Exception as e:
    print(f"Error cleaning dataframe column names: {e}")
    raise
  
  try:
    # Remove leading/trailing whitespace from strings
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    print(f"Removed leading/trailing whitespace from strings on dataframe.")
    
  except Exception as e:
    print(f"Error removing leading/trailing whitespace from dataframe: {e}")
    raise

  try:
    # Infer data types
    df = infer_data_types(df)
    
  except Exception as e:
    print(f"Error inferring data types from dataframe: {e}")
    raise
  
  try:
    # Fill missing values accordingly
    df = fill_na_by_dtype(df)
    
  except Exception as e:
    print(f"Error filling out null values in dataframe: {e}")
    raise
    
  # Return clean dataframe
  return df

def infer_data_types(df: pd.DataFrame) -> pd.DataFrame:
  """
  Infer data types of a Pandas dataframe.
  
  Parameters: 
  df (pd.DataFrame): Pandas dataframe to clean
  
  Returns: 
  pd.DataFrame: Dataframe with inferred datatype
  """
  
  for col in df.columns:
    try:
      # Try to convert to a numeric field
      df[col] = pd.to_numeric(df[col])
      continue
    
    except (ValueError, TypeError) as e:
      pass
    
    try:
      # Try to convert to a datetime field
      df[col] = pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S')
      continue
    
    except (ValueError, TypeError) as e:
      pass
    
    try:
      # Try to convert to a boolean field
      
      # First, check if all non-null values are True/False strings
      is_bool_col = df[col].dropna().apply(lambda x: str(x).strip().lower()).isin(['true', 'false']).all()
      
      if is_bool_col:
        df[col] = df[col].apply(lambda x: True if str(x).strip().lower() == 'true' else (False if str(x).strip().lower() == 'false' else pd.NA))
        df[col] = df[col].astype('boolean')
        
      continue
    
    except (ValueError, TypeError) as e:
      pass
    
    #If not, convert column to string
    df[col] = df[col].astype(str, errors="ignore")
    
  print(f"Dataframe datatypes inferred.")
    
  return df

def fill_na_by_dtype(df: pd.DataFrame) -> pd.DataFrame:
  """
  Fill null values depending on the data type
  
  Parameters: 
  df (pd.DataFrame): Pandas dataframe to fill
  
  Returns: 
  pd.DataFrame: Filled dataframe
  """ 
  
  #Iterate through the data types in the dataframe
  for col, dtype in df.dtypes.items(): 
    
    try:
      dtype_str = dtype.name.lower()
      
      # Fill null values based on data type
      # Note: Using startswith because Pandas can have int32, int64, datetime64[ns], etc. 
      if dtype_str.startswith('int'):
        df[col] = df[col].fillna(0)
      elif dtype_str.startswith('float'):
        df[col] = df[col].fillna(0.0)
      elif dtype_str.startswith('bool'):
        df[col] = df[col].fillna(pd.NA)
      elif dtype_str.startswith(('datetime', 'date')):
        df[col] = df[col].fillna(pd.NaT)
      else:
        df[col] = df[col].fillna('')
    
    except Exception as e:
      print(f"Error filling out null values in column {col}: {e}")
      raise
   
  print(f"Dataframe null values filled.")
   
  return df

def generate_schema_from_dataframe(df: pd.DataFrame, table_name: str) -> str:
  """
  Generate a schema from a Pandas dataframe. 
  
  Parameters: 
  df (pd.DataFrame): Pandas dataframe to generate schema from 
  table_name (str): Name of table
  
  Returns: 
  str: String representing table schema
  """
  
  col_types = []
  
  #Iterate through the data types in the dataframe and add to list
  for col, dtype in df.dtypes.items(): 
    dtype_str = dtype.name.lower()
    
    # Map to a SQL type
    # Note: Using startswith because Pandas can have int32, int64, datetime64[ns], etc. 
    if dtype_str.startswith('int'):
      sql_type = 'INTEGER'
    elif dtype_str.startswith('float'):
      sql_type = 'REAL'
    elif dtype_str.startswith('bool'):
      sql_type = 'BOOLEAN'
    elif dtype_str.startswith('datetime'):
      sql_type = 'DATETIME'
    elif dtype_str.startswith('date'):
      sql_type = 'DATE'
    else:
      sql_type = 'TEXT'
    
    col_types.append(f'{col.lower()} {sql_type}')
  
  #Create a string from the list that represents the schema
  schema = f"CREATE TABLE {table_name} ({', '.join(col_types)});"
  print(f"Schema inferred from dataframe: {schema}")
  return schema