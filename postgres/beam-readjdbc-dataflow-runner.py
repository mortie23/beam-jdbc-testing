import os
from dotenv import load_dotenv
import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc

# from apache_beam.typehints.schemas import LogicalType
# from apache_beam import coders
# from typing import NamedTuple

# JSON key file in an environment variable
# export GOOGLE_APPLICATION_CREDENTIALS="key.json"

load_dotenv()
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOSTNAME = os.getenv("PG_HOSTNAME")
GCP_PROJECT_NAME = os.getenv("GCP_PROJECT_NAME")

# Define your Dataflow options
options = {
    "project": f"{GCP_PROJECT_NAME}",
    "job_name": "read-postgres-else",
    "staging_location": "gs://xyz-beam-test/staging",
    "temp_location": "gs://xyz-beam-test/temp",
    "runner": "DataflowRunner",
    "region": "australia-southeast1",  # Change to your desired region
}

with beam.Pipeline(options=beam.pipeline.PipelineOptions.from_dictionary(options)) as p:
    result = (
        p
        | "Read from jdbc"
        >> ReadFromJdbc(
            table_name="mortimer_nfl.quarterback",
            driver_class_name="org.postgresql.Driver",
            jdbc_url=f"jdbc:postgresql://{PG_HOSTNAME}:5432/mortimer_dev",
            username="postgres",
            password=PG_PASSWORD,
        )
        | "Print the results" >> beam.Map(print)
    )
