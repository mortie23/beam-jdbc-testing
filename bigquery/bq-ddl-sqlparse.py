# %%
import sqlparse

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
