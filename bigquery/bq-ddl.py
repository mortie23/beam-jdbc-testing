# %%
import sqlparse
from google.cloud import bigquery

client = bigquery.Client()


# %%
sql_statement = """
create table schema.test (
  col1 int
  , col2 char
)
;
"""
parsed = sqlparse.parse(sql_statement)
parsed

create_table_statement = parsed[0]

# %%
# Perform a query.
QUERY = """
SELECT 
    name 
FROM 
    `bigquery-public-data.usa_names.usa_1910_2013` 
WHERE 
    state = "TX" 
LIMIT 100
"""
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(row.name)


# %%

# Your SQL statement
sql = """
create table [schema].[test] (
  [col1] int
  , [col2] char
  , [column with a space] nvarchar(max)
)
;"""

# Parse the SQL statement
parsed = sqlparse.parse(sql)

# Get the 'create table' statement
stmt = parsed[0]
breakpoint()
# Extract the table name
fully_qualified_object_name = None

# Extract the parenthesis which contains column details
parenthesis = None
for token in stmt.tokens:
    if isinstance(token, sqlparse.sql.Identifier):
        fully_qualified_object_name = token.value
    if isinstance(token, sqlparse.sql.Parenthesis):
        parenthesis = token

# Check if parenthesis is not None
if parenthesis is not None:
    # Extract the column definitions
    columns = parenthesis.tokens

    # Initialize a dictionary to hold column names and types
    column_dict = {}

    # Iterate over the column definitions
    for i in range(len(columns)):
        if isinstance(columns[i], sqlparse.sql.Identifier):
            # Split the column definition into name and type
            name = columns[i].value
            # Add to the dictionary
            column_dict[name] = (
                columns[i + 2].value
                if isinstance(columns[i + 2], sqlparse.sql.Token)
                else None
            )

    print(f"Table Name: {fully_qualified_object_name}")
    print("Columns:")
    for name, type in column_dict.items():
        print(f"{name}: {type}")
else:
    print("No column details found in the SQL statement.")


# %%
