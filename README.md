# SQL Query Generation and Natural Language Response using Generative AI

This project demonstrates how to use a generative AI model to answer questions based on data stored in a MySQL database. By leveraging a language model (LLM), we can generate SQL queries to retrieve information from the database and then convert the results into natural language responses.

## Table of Contents
- Setup
- How It Works
- Code Explanation and Example Usage

## Setup

### Prerequisites
- Python 3.12
- MySQL database
- Azure OpenAI credentials

### Installation
1. Clone the repository
2. Install the required packages
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your MySQL database and update the connection URI in the code:
    ```python
    mysql_uri = 'mysql+mysqlconnector://root:your_password@localhost:3306/Chinook'
    ```

4. Set up your Azure OpenAI credentials:
    ```python
    AZURE_OPENAI_ENDPOINT = "https://your_azure_openai_endpoint.openai.azure.com/"
    AZURE_OPENAI_KEY = "your_azure_openai_key"
    CHAT_COMPLETION_NAME = "gpt-4o-mini"
    API_VERSION = "2024-08-01-preview"
    ```

## How It Works

1. **Initialize AzureChatOpenAI Client**:
    - Set up the client with necessary credentials to interact with Azure OpenAI.

2. **Connect to MySQL Database**:
    - Establish a connection to the MySQL database to retrieve schema information.

3. **Generate SQL Query**:
    - Use a template to instruct the LLM to generate an SQL query based on the database schema and user's question.

4. **Run SQL Query**:
    - Execute the generated SQL query against the database to get the result.

5. **Generate Natural Language Response**:
    - Use another template to instruct the LLM to generate a natural language response based on the schema, question, SQL query, and SQL response.

6. **Full Chain Execution**:
    - Combine all steps into a full chain to generate the SQL query, run it, and produce a user-friendly answer.
  
## Code Explanation and Example Usage

We actually need two chains, one for generating the SQL query and the second to create the natural language response:

## 1. SQL Query Generation Chain

- First, we need to create a chain that instructs the LLM to generate an SQL query based on the database schema and the user's question.

- It uses a template like this:
  ```python
  template = """Based on the table schema below, write a SQL query that would answer the user's question:
  {schema}

  Question: {question}
  SQL Query:"""
  prompt = ChatPromptTemplate.from_template(template)

Then, we provide the input data:

```python
input_data = {"question": "Generate an SQL query to find out how many artists are there in the `artist` table."}
```

The output after parsing will be the SQL query like this:

```sql
SELECT COUNT(*) AS NumberOfArtists FROM artist;
```

The LLM generates the SQL query to answer the user's question.

This chain instructs the LLM to generate a natural language response based on the schema, question, SQL query, and SQL response.

Example template:

```python
template = """Based on the table schema below, question, sql query and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}"""
prompt = ChatPromptTemplate.from_template(template)
```

Using the invoke method to get the final output:

```python
full_chain = (
    RunnablePassthrough.assign(query=lambda vars: parse_sql_output(sql_chain.invoke(vars).content)).assign(
        schema=get_schema,
        response=lambda vars: run_query(vars["query"]),
    )
    | prompt
    | llm
)
```

The output will be something like:

```text
"Based on the data in the artist table, there are a total of 275 artists."
```
The number 275 actually comes from the first chain from the SQL query result:

```sql
SELECT COUNT(*) AS NumberOfArtists FROM artist;
```
