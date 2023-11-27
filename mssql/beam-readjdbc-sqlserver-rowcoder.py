import os
from dotenv import load_dotenv
import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc
from typing import NamedTuple
from apache_beam.coders import registry, RowCoder
from apache_beam.typehints.schemas import LogicalType

load_dotenv()
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")
MSSQL_HOSTNAME = os.getenv("MSSQL_HOSTNAME")


@LogicalType.register_logical_type
class JdbcBit(LogicalType[int, int, int]):
    @classmethod
    def urn(cls):
        return "beam:logical_type:javasdk_bit:v1"

    @classmethod
    def language_type(cls):
        return int

    def to_language_type(self, value):
        return int

    def to_representation_type(self, value):
        return int


class BadRow(NamedTuple):
    id_col: int
    first_name: str
    is_bit: JdbcBit


registry.register_coder(BadRow, RowCoder)


with beam.Pipeline() as p:
    rows = (
        p
        | "Read from JDBC"
        >> ReadFromJdbc(
            table_name="cwms.test_row_coder",
            driver_class_name="com.microsoft.sqlserver.jdbc.SQLServerDriver",
            classpath=["com.microsoft.sqlserver:mssql-jdbc:11.2.2.jre8"],
            jdbc_url=f"jdbc:sqlserver://{MSSQL_HOSTNAME}:1433;Database=mortimer_dev;trustServerCertificate=true;",
            username="sa",
            password=MSSQL_PASSWORD,
        )
        | "Print rows" >> beam.Map(print)
    )
