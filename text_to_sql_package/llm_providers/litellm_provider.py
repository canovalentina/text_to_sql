import litellm
import time
from text_to_sql_package.llm_providers.llm_provider import LLMProvider

class LiteLLMProvider():
    
  def __init__(self, model_name: str):
    """
    Class constructor.
    
    Parameters:
    model_name (str): Name of the LLM model
    """
    print(f"LiteLLM provider using the following model: {model_name}.")
    self.model_name = model_name
  
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
    
    print(f"Generating SQL query using LiteLLM for user prompt '{user_prompt}'...")

    # Create the message for the LLM in LiteLLM format
    message = f"""
    Generate a SQL query for the prompt "{user_prompt}", based on the following table schema:
    {schema}
    
    Provide ONLY the query, without any explanation. I need to be able to copy paste it into a SQL engine.
    Do not add any backticks and do not start with the word sql.
    """
    
    # To avoid rate limit, only retry a set number of times
    for i in range(max_retries):
      try:
        # Send message to the LLM
        response = litellm.completion(model=self.model_name, messages=[{"content": message, "role": "user"}])
        
        # Grab first choice from the LLM and access the text content
        result = response.choices[0].message.content
        
        print(f"SQL query generated: {result}")
      
        return result
      
      except litellm.RateLimitError as e:
        time.sleep(initial_delay)
        #Increase delay
        initial_delay *= 2
      
      except Exception as e:
        print(f"Error querying LLM {self.model_name}: {e}") 
        raise


