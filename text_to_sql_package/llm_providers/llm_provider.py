from typing import Protocol

class LLMProvider(Protocol):
  
  """Interface for classes that handle LLM provisions and natural language prompt to SQL query conversion."""
    
  def generate_sql_query(self, user_prompt: str, schema: str, max_retries: int = 3, initial_delay: int = 1) -> str:
    """
    Using an LLM, generate a SQL to query a dataset based on a user prompt.
    
    Parameters:
    user_prompt (str): Natural language prompt to query the dataset.
    schema (str): Table schema for the SQL query
    max_retries (int): Max number of times that the LLM can retry. Optional
    initial_delay (int): Initial delay between each retry. Optional

    Returns:
    str: SQL query
    """
    ...