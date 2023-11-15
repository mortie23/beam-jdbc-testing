import os
from dotenv import load_dotenv
import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc

# If environment has this and want to test a local runner need to unset
# unset GOOGLE_APPLICATION_CREDENTIALS

load_dotenv()
TD_PASSWORD = os.getenv("TD_PASSWORD")
TD_HOSTNAME = os.getenv("TD_HOSTNAME")

with beam.Pipeline() as p:
    result = (
        p
        | "Read from jdbc"
        >> ReadFromJdbc(
            table_name="demo_user.testing",
            driver_class_name="com.teradata.jdbc.TeraDriver",
            jdbc_url=f"jdbc:teradata://{TD_HOSTNAME}/database=demo_user,tmode=ANSI",
            username="demo_user",
            password=TD_PASSWORD,
            driver_jars="/tmp/terajdbc4.jar",
            classpath=["/tmp/terajdbc4.jar"],
        )
        | "Print the results" >> beam.Map(print)
    )
