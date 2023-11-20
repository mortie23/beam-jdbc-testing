# %%
import pandas as pd
from google.cloud import bigquery
from dbtype import *

client = bigquery.Client()
# %%
# A dump from Teradata DBC.ColumnsV
df = pd.read_csv("td-object-schemas.csv", keep_default_na=False)
df["ColumnType"] = df["ColumnType"].str.strip()
df = df.astype(
    {"ColumnLength": str, "DecimalTotalDigits": str, "DecimalFractionalDigits": str}
)

# %%
type_mapping = pd.read_csv("type-mapping.csv", keep_default_na=False)
td_type_mapping = type_mapping[type_mapping["source_system"] == "teradata"]


# %%
df["TdDDLFullType"] = df.apply(
    lambda x: td_ddl_full_type(
        x["ColumnType"],
        x["ColumnLength"],
        x["DecimalTotalDigits"],
        x["DecimalFractionalDigits"],
    ),
    axis=1,
)

df["TdType"] = df.apply(
    lambda x: td_type(
        x["ColumnType"],
    ),
    axis=1,
)

# %%
table_list = df[["DatabaseName", "TableName"]].drop_duplicates().reset_index(drop=True)

# %%
for index, row in table_list.iterrows():
    print(row["DatabaseName"], row["TableName"])
    ddl = bq_ddl(
        df[
            (df["DatabaseName"] == row["DatabaseName"])
            & (df["TableName"] == row["TableName"])
        ].reset_index(drop=True),
        td_type_mapping,
    )
    with open(f"ddl/{row['DatabaseName']}.{row['TableName']}.sql", "w") as file:
        file.write(ddl)
    # Create table on BigQuery
    drop_table = f"drop table if exists {row['DatabaseName']}.{row['TableName']}"
    drop_job = client.query(drop_table)
    create_job = client.query(ddl)
