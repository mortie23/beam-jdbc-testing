#!/bin/bash
#
# Creates a flex template for a the loadtdtable test Beam pipeline
# Usage
#    ./build.sh --env dev

source helpers.sh
# Parse arguments
parse_args "$@"

# Ensure the argument existed when the script was called
if [[ -z ${env} ]]; then
    error_code=1
    echo "ERROR" "environment was not provided"
    exit ${error_code}
fi

# Configuration for environment
eval $(parse_config config.yml $env)
# Set the active project foir environment
echo ${project_id}
gcloud config set project ${project_id}

# Build a Docker image
docker build -t ${artifact_registry}/${project_id}/${artifact_repo_docker}/dataflow/loadtdtable:0.7 .
# Authenticate with the registry
gcloud auth configure-docker ${artifact_registry}
# Push to registry
docker push ${artifact_registry}/${project_id}/${artifact_repo_docker}/dataflow/loadtdtable:0.7

# Create Flex Template from already build and pushed container image
gcloud dataflow flex-template build gs://${storage_bucket}/dataflow/flex-template/loadtdtable.json \
    --image "${artifact_registry}/${project_id}/${artifact_repo_docker}/dataflow/loadtdtable:0.7" \
    --sdk-language "PYTHON" \
    --metadata-file "metadata.json" \
    --staging-location "gs://${storage_bucket}/dataflow/staging" \
    --temp-location "gs://${storage_bucket}/dataflow/temp"
