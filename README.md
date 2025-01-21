# Text to SQL

## Assignment

Using best OOP principles and design patterns, create a python package, for Text – to – SQL use case, that will be LLM model agnostic.

The business logic -> from any given dataset (xls/csv/tsv file), allow for user to prompt with natural language, and extract rows in a form of list of validate jsons.

The package has to:

1. Implement abstractions/interfaces.
2. Heavily based on dependency injection of interfaces
3. Implement connecting to LLM providers, through defined abstractions
4. Implement connecting to SQL Databases through defined abstractions
5. Main abstraction, should be just a function that will take user prompt, and path to file as input

**Stack to consider**: SQLite, LiteLLM/DSPy, Pydantic

**Stack to avoid**: Any high level wrappers, such as LangChain or LlamaIndex

**Approaches to consider**: Function calling, structured outputs

## Implementation details

#### Defining Protocols

For this project, I used Python Protocols to define interfaces.

I focused on 4 Protocols, which are each neatly organized in a folder with any implementing classes.

1. `DataLoader`: handles data load operations. Implemented by: CSVLoader, TSVLoader and ExcelLoader.
2. `DataValidator`: handles data validation. Implemented by: PydanticValidator.
3. `DatabaseConnector`: handles connection and querying from a SQL database. Implemented by: SQLiteDatabaseConnector.
4. `LLMProvider`: handles LLM provisions and natural language prompt to SQL query conversion. Implemented by: LiteLLMProvider.

### LLM-Agnostic

LiteLLMProvider allows access to a wide variety of LLMs, making this implementation LLM agnostic

#### Utils

I created a utils folder with two files that contains helper functions:

1. `dataframe_utils.py`: Functions for manipulating dataframes, related to cleaning data and inferring data types
2. `file_utils.py`: Functions related to file validation and creation (checking whether they exist, have the correct file extension, etc.)

#### TextToSQL

In the `TextToSQL` class everything comes together to be able to carry out the package's goal.

This class uses a `DataLoader`, a `DataValidator`, a `DatabaseConnector`, and an `LLMProvider`, following the dependency injection principle.

It contains several helper functions to organize the code. Ultimately, the primary function `extract_data_from_file_with_prompt(file_path, user_prompt)` allows the user to query a file using a natural language prompt.

### Output

The extracted data is a string which contains the list of validated JSONs. To copy it to a JSON file, I created the helper function `save_json_to_file(json_str, file_path)`.

For example, in `test.py`, I ran `save_json_to_file(json_str=result, file_path=replace_file_type_with_json(file_path))` to save the query output into a JSON file which has the same name as the original file (e.g. family.csv -> family.json)

## How to test

#### LLM Set up

Set the environment variables to the `MODEL_NAME` and an `API_KEY` that you can authenticate an LLM.

For example, I used "gemini-1.5-flash" and a `GOOGLE_API_KEY`.
Other options are available here: https://docs.litellm.ai/

#### Set up the file path and user prompt

Provide the file path with the data set and the natural language prompt to query the database in the `test.py` file.

Then, run `python test.py` in the terminal.

For example, I selected:
`file_path = "sample_data/family.csv"`
`user_prompt = "Give me information on all female members of my family.`

The results of my test are in sample_data/family.json.

## Future considerations

Due to time constraints, the scope of this project was limited.
Future iterations should include:

- Handling of followup prompts. This would require storing the previous prompt and answers in memory.
- Testing
- A Command-line interface, API layer or web interface to run the package more easily.
