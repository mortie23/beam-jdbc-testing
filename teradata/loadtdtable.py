"""Testing a basic write to BigQuery
"""

from __future__ import annotations

import argparse
import logging

import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import secretmanager


def access_secret(
    project_id: str,
    secret_id: str,
    version_id: int = 1,
) -> str:
    """Get a secret and return as string

    Args:
        project_id (str): GCP Project ID
        secret_id (str): The name of the secret
        version_id (int, optional): version of API. Defaults to 1.

    Returns:
        str: _description_
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


SCHEMA = ",".join(
    [
        "FRUIT_NAME:STRING",
        "FRUIT_TYPE:STRING",
    ]
)


def run(
    table_name: str,
    schema_name: str,
    prjid: str,
    beam_args: list[str] = None,
) -> None:
    """Build and run the pipeline."""
    options = PipelineOptions(beam_args, save_main_session=True)

    teradata_clearscape_password = access_secret(
        project_id=prjid, secret_id="teradata_clearscape_password"
    )
    teradata_clearscape_host = access_secret(
        project_id=prjid, secret_id="teradata_clearscape_host"
    )

    with beam.Pipeline(options=options) as pipeline:
        pCollection = pipeline | "Read from jdbc" >> ReadFromJdbc(
            table_name=f"{schema_name}.{table_name}",
            driver_class_name="com.teradata.jdbc.TeraDriver",
            jdbc_url=f"jdbc:teradata://{teradata_clearscape_host}/database=demo_user,tmode=ANSI",
            username="demo_user",
            password=teradata_clearscape_password,
            driver_jars="/template/terajdbc4.jar",
            classpath=["/template/terajdbc4.jar"],
        )
        # Output the results into BigQuery table.
        _ = pCollection | "Write to Big Query" >> beam.io.WriteToBigQuery(
            f"{schema_name}.{table_name}",
            schema=SCHEMA,
        )
        print(table_name, schema_name, prjid, teradata_clearscape_host)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--table_name", help="the name of the source system table and target table"
    )
    parser.add_argument(
        "--schema_name",
        help="the name of the source system database and target dataset",
    )
    parser.add_argument(
        "--prjid",
        help="the name of the source system database and target dataset",
    )
    args, beam_args = parser.parse_known_args()
    print(args)
    print(beam_args)
    run(
        table_name=args.table_name,
        schema_name=args.schema_name,
        prjid=args.prjid,
        beam_args=beam_args,
    )
