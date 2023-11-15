import apache_beam as beam

with beam.Pipeline() as p:
    pass

beam_options = PipelineOptions(
    runner="DataflowRunner",
    project=f"{GCP_PROJECT_NAME}",
    job_name="a-job-name",
    temp_location="gs://xyz-beam-test/tmp",
)
