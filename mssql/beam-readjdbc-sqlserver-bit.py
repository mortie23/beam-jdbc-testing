import os
from dotenv import load_dotenv
import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc
from typing import NamedTuple
from apache_beam.coders import Coder, registry, RowCoder

load_dotenv()
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")
MSSQL_HOSTNAME = os.getenv("MSSQL_HOSTNAME")


class BitCoder(Coder):
    def encode(self, value):
        return b"\x01" if value else b"\x00"

    def decode(self, value):
        return value == b"\x01"


# Register the coder for the BIT type
registry.register_coder(bool, BitCoder)

ExampleRow = NamedTuple(
    "ExampleRow",
    [
        ("id_col", int),
        ("first_name", str),
        ("is_bit", bool),
    ],
)
registry.register_coder(ExampleRow, RowCoder)


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
