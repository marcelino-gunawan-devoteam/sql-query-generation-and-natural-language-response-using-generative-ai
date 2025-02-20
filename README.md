# SQL Query Generation and Natural Language Response using Generative AI

This project demonstrates how to use a generative AI model to answer questions based on data stored in a MySQL database. By leveraging a language model (LLM), we can generate SQL queries to retrieve information from the database and then convert the results into natural language responses.

## Table of Contents
- Setup
- How It Works
- Code Explanation
- Example Usage

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
