# %%
import pandas as pd
from google.cloud import bigquery
from dbtype import *

client = bigquery.Client()

db_type = "mssql"
# %%
df = object_schema(f"{db_type}-object-schemas.csv", db_type)

# %%
type_mapping = pd.read_csv("type-mapping.csv", keep_default_na=False)
type_mapping = type_mapping[type_mapping["source_system"] == db_type]

if db_type == "teradata":
    df["source_type"] = df.apply(
        lambda x: teradata_type(
            x["ColumnType"],
        ),
        axis=1,
    )
elif db_type == "mssql":
    df["source_type"] = df["ColumnType"]

# %%
table_list = df[["DatabaseName", "TableName"]].drop_duplicates().reset_index(drop=True)

# %%
for index, row in table_list.iterrows():
    print(row["DatabaseName"], row["TableName"])
    breakpoint()
    ddl = bq_ddl(
        df[
            (df["DatabaseName"] == row["DatabaseName"])
            & (df["TableName"] == row["TableName"])
        ].reset_index(drop=True),
        type_mapping,
    )
    with open(f"ddl/{row['DatabaseName']}.{row['TableName']}.sql", "w") as file:
        file.write(ddl)
    # Create table on BigQuery
    drop_table = f"drop table if exists {row['DatabaseName']}.{row['TableName']}"
    drop_job = client.query(drop_table)
    create_job = client.query(ddl)

# %%
