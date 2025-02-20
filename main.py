from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_community.utilities import SQLDatabase

# Define the parsing function to extract the SQL query from the LLM's response
def parse_sql_output(output):#
    if '```sql' in output:
        return output.split('```sql')[1].split('```')[0].strip()
    return output


# Azure OpenAI configuration
AZURE_OPENAI_ENDPOINT = "https://your_azure_openai_endpoint.openai.azure.com/"
AZURE_OPENAI_KEY = "your_azure_openai_key"
CHAT_COMPLETION_NAME = "gpt-4o-mini"
API_VERSION = "2024-08-01-preview"

# Initialize the AzureChatOpenAI client
azure_llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version=API_VERSION,
    azure_deployment=CHAT_COMPLETION_NAME
)


llm = azure_llm
llm = llm.bind(stop=["```\n"])#

# Initialize the database connection
mysql_uri = 'mysql+mysqlconnector://root:your_password@localhost:3306/Chinook'
db = SQLDatabase.from_uri(mysql_uri)

def get_schema(_=None):
    schema = db.get_table_info()
    return schema

# Define the template
template = """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:"""
prompt = ChatPromptTemplate.from_template(template)

# Create the SQL chain
sql_chain = (RunnablePassthrough.assign(schema=get_schema) | prompt | llm)


# Invoke the chain with the refined prompt
input_data = {"question": "Generate an SQL query to find out how many artists are there in the `artist` table."}
raw_output = sql_chain.invoke(input_data)
parsed_output = parse_sql_output(raw_output.content)
print("Final SQL query:", parsed_output)


# Define the template for generating natural language response
template = """Based on the table schema below, question, sql query and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}"""
prompt = ChatPromptTemplate.from_template(template)

def run_query(query):
    return db.run(query)

# Create the full chain
full_chain = (
    RunnablePassthrough.assign(query=lambda vars: parse_sql_output(sql_chain.invoke(vars).content)).assign(
        schema=get_schema,
        response=lambda vars: run_query(vars["query"]),
    )
    | prompt
    | llm
)

# Invoke the chain with the refined prompt
input_data = {"question": "how many artists are there?"}
raw_output = sql_chain.invoke(input_data)
print("Raw output from SQL chain:", raw_output)

parsed_output = parse_sql_output(raw_output.content)
print("Parsed SQL query:", parsed_output)

# Add parsed query to input data
input_data["query"] = parsed_output
input_data["schema"] = get_schema()
input_data["response"] = run_query(parsed_output)

# Print input data before invoking the full chain
print("Input data for full chain:", input_data)

# Invoke the full chain
result = full_chain.invoke(input_data)
print("Final result:", result.content)











