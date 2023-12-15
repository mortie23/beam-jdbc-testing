#!/bin/bash
#
# Unit tests for the helpers.sh script
# Usage
#    ./build.sh --env dev --name hellofruit

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
eval $(parse_config config-test.yml $env)
echo ${env_resolve}
echo ${name}
