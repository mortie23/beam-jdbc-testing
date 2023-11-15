# %%
import os
from dotenv import load_dotenv
import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc

# If environment has this and want to test a local runner need to unset
# unset GOOGLE_APPLICATION_CREDENTIALS

load_dotenv()
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")
MSSQL_HOSTNAME = os.getenv("MSSQL_HOSTNAME")


with beam.Pipeline() as p:
    result = (
        p
        | "Read from jdbc"
        >> ReadFromJdbc(
            table_name="cwms.test_working_types",
            driver_class_name="com.microsoft.sqlserver.jdbc.SQLServerDriver",
            classpath=["com.microsoft.sqlserver:mssql-jdbc:11.2.2.jre8"],
            jdbc_url=f"jdbc:sqlserver://{MSSQL_HOSTNAME}:1433;Database=mortimer_dev;trustServerCertificate=true;",
            username="sa",
            password=MSSQL_PASSWORD,
        )
        | beam.Map(print)
    )
