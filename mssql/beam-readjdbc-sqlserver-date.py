import os
from dotenv import load_dotenv
import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc
from apache_beam.typehints.schemas import MillisInstant
from apache_beam.typehints.schemas import LogicalType

LogicalType.register_logical_type(MillisInstant)

load_dotenv()
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")
MSSQL_HOSTNAME = os.getenv("MSSQL_HOSTNAME")

with beam.Pipeline() as p:
    rows = (
        p
        | "Read from JDBC"
        >> ReadFromJdbc(
            table_name="cwms.test_date",
            driver_class_name="com.microsoft.sqlserver.jdbc.SQLServerDriver",
            classpath=["com.microsoft.sqlserver:mssql-jdbc:11.2.2.jre8"],
            jdbc_url=f"jdbc:sqlserver://{MSSQL_HOSTNAME}:1433;Database=mortimer_dev;trustServerCertificate=true;",
            username="sa",
            password=MSSQL_PASSWORD,
        )
        | "Print rows" >> beam.Map(print)
    )
