import apache_beam as beam
from apache_beam.transforms.sql import SqlTransform

# Define a sample input data as a list of dictionaries
input_data = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 101, "name": "Carol"},
    {"id": 102, "name": "David"},
]

# Create a pipeline
with beam.Pipeline() as p:
    # Read input data and convert it to a PCollection of Rows
    input_rows = (
        p
        | "Create input data" >> beam.Create(input_data)
        | "Convert to Rows"
        >> beam.Map(lambda x: beam.Row(id=int(x["id"]), name=str(x["name"])))
    )

    # Apply the SQL transform
    filtered_rows = input_rows | SqlTransform(
        "SELECT id, name FROM PCOLLECTION WHERE id > 100"
    )

    # Print the results
    filtered_rows | "Print results" >> beam.Map(print)
