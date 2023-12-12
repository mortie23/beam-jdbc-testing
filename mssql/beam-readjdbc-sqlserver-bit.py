import os
from dotenv import load_dotenv
import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc
from apache_beam.typehints.schemas import LogicalType


@LogicalType.register_logical_type
class bit_type(LogicalType):
    def __init__(self, LogicalType):
        self.LogicalType = LogicalType

    @classmethod
    def urn(cls):
        return "beam:logical_type:javasdk_bit:v1"

    @classmethod
    def language_type(cls):
        return bool

    def to_language_type(self, value):
        return bool(value)

    def to_representation_type(self, value):
        return bool(value)


load_dotenv()
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")
MSSQL_HOSTNAME = os.getenv("MSSQL_HOSTNAME")

with beam.Pipeline() as p:
    rows = (
        p
        | "Read from JDBC"
        >> ReadFromJdbc(
            table_name="cwms.test_bit",
            driver_class_name="com.microsoft.sqlserver.jdbc.SQLServerDriver",
            classpath=["com.microsoft.sqlserver:mssql-jdbc:11.2.2.jre8"],
            jdbc_url=f"jdbc:sqlserver://{MSSQL_HOSTNAME}:1433;Database=mortimer_dev;trustServerCertificate=true;",
            username="sa",
            password=MSSQL_PASSWORD,
        )
        | "Print rows" >> beam.Map(print)
    )
