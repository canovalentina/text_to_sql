import os
import json

def check_file_exists(file_path: str):
  """
  Check if a file exists. If not, raise exception.
  
  Parameters:
  file_path (str): File path to given dataset
  """
  
  if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")
  else:
    print(f"File exists: {file_path}")
    
def check_file_type(file_path: str, file_types: str):
  """
  Check if correct file_type. If not, raise exception.
  
  Parameters:
  file_path (str): File path to given dataset
  """

  # Check if the file path ends in one of the specified file type(s)
  if not any(file_path.lower().endswith(ft) for ft in file_types):
    raise ValueError(f"The provided file must end in {','.join(file_types)}")
  else:
    print(f"File type acceptable: {file_path}")

def replace_file_type_with_json(file_path: str):
  """
  Replaces file name type to JSON, but maintaining the original file path.
  
  Parameters:
  file_path (str): File path to given dataset (e.g. /docs/test.csv)
  
  Returns:
  str: New file path, with substituted file type (e.g. /docs/test.json)
  """
  
  path, file_type = os.path.splitext(file_path)
  return f"{path}.json"
  
def save_json_to_file(json_str: str, file_path: str) -> None:
  """
  Write JSON string into a file.
  
  Parameters:
  json_str(str): String of JSON object
  file_path (str): File path to output JSON to
  """
  
  try:
    #Parse valid JSON string and converts it to Python object
    json_data = json.loads(json_str)
    
    with open(file_path, "w") as file:
      json.dump(json_data, file)
      
    print(f"JSON file created: {file_path}")
    
  except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    raise
  
  except Exception as e:
    print(f"Error saving JSON to {file_path}: {e}")
    raise
  
    