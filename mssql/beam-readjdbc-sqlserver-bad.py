# %%
import os
from dotenv import load_dotenv
import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc
from apache_beam.typehints.schemas import LogicalType
import typing
from apache_beam import coders

# If environment has this and want to test a local runner need to unset
# unset GOOGLE_APPLICATION_CREDENTIALS

load_dotenv()
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")
MSSQL_HOSTNAME = os.getenv("MSSQL_HOSTNAME")


class BitType(LogicalType):
    def __init__(self):
        super(BitType, self).__init__()

    def to_base_type(self, bit):
        return bool(bit)

    def to_input_type(self, boolean):
        return int(boolean)


# Define your table schema as a NamedTuple
MyTableRow = typing.NamedTuple(
    "MyTableRow",
    [
        ("test_bit", BitType),  # Use BitType for bit columns
        # Define other columns here
    ],
)

# Register the coder for your table row
coders.registry.register_coder(MyTableRow, coders.RowCoder)


with beam.Pipeline() as p:
    result = (
        p
        | "Read from jdbc"
        >> ReadFromJdbc(
            table_name="cwms.test_bad_types",
            driver_class_name="com.microsoft.sqlserver.jdbc.SQLServerDriver",
            classpath=["com.microsoft.sqlserver:mssql-jdbc:11.2.2.jre8"],
            jdbc_url=f"jdbc:sqlserver://{MSSQL_HOSTNAME}:1433;Database=mortimer_dev;trustServerCertificate=true;",
            username="sa",
            password=MSSQL_PASSWORD,
            coder=coders.RowCoder(MyTableRow),
        )
        | beam.Map(print)
    )

# %%
