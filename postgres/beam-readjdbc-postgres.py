import os
from dotenv import load_dotenv
import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc

# If environment has this and want to test a local runner need to unset
# unset GOOGLE_APPLICATION_CREDENTIALS

load_dotenv()
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOSTNAME = os.getenv("PG_HOSTNAME")

with beam.Pipeline() as p:
    result = (
        p
        | "Read from jdbc"
        >> ReadFromJdbc(
            table_name="mortimer_nfl.sanfran",
            driver_class_name="org.postgresql.Driver",
            jdbc_url=f"jdbc:postgresql://{PG_HOSTNAME}:5432/mortimer_dev",
            username="postgres",
            password=PG_PASSWORD,
        )
        | beam.Map(print)
    )
