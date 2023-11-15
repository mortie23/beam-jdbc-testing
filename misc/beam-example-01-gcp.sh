# this one works after setting up the service account and exporting the location of the 
# JSON key file in an environment variable
# export GOOGLE_APPLICATION_CREDENTIALS="key.json"
python -m apache_beam.examples.wordcount \
  --input gs://dataflow-samples/shakespeare/kinglear.txt \
  --output gs://xyz-beam-test/counts \
  --runner DataflowRunner \
  --project $GCP_PROJECT_NAME \
  --region australia-southeast1 \
  --temp_location gs://xyz-beam-test/tmp/
