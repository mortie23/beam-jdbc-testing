# %%
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# %%
load_dotenv()
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOSTNAME = os.getenv("PG_HOSTNAME")

# %%
# Establish a connection to the database
connection = psycopg2.connect(
    dbname="mortimer_dev",
    user="postgres",
    host=PG_HOSTNAME,
    password=PG_PASSWORD,
)

# %%
# Execute a SELECT statement
sql = "SELECT * FROM mortimer_nfl.sanfran"

# Use pandas to execute the query and store the result in a DataFrame
df = pd.read_sql_query(sql, connection)

# %%
