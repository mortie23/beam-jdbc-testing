# Building a custom Dataflow flex template

## Options

### Using the build script

The build script will run the extra steps for you:

```sh
./build.sh --env dev
```

### Manual step by step

Build the Docker image on your local client development machine, tagging the image with the full reference to the GCP Artifact registry repository.

```sh
docker build . -t australia-southeast1-docker.pkg.dev/<project_id>/<artifact_repository_docker>/dataflow/hellofruit:0.1
```

Before you try to push the container image to the Artifact registry repository you need to authenticate your `gcloud` CLI with the artifact registry.

```sh
gcloud auth configure-docker australia-southeast1-docker.pkg.dev
```

Push the image to the registry.

```sh
docker push australia-southeast1-docker.pkg.dev/<project_id>/<artifact_repository_docker>/dataflow/hellofruit:0.1
```

Now we can build a flex template.

```sh
gcloud dataflow flex-template build "gs://<storage_bucket>/dataflow/flex-template/hellofruit.json" \
     --image "australia-southeast1-docker.pkg.dev/<project-id>/<artifact_repository_docker>/dataflow/hellofruit:0.1" \
     --sdk-language "PYTHON" \
     --metadata-file "metadata.json"
```

This should run quite quickly and result in a JSON file in the bucket location you requested.

```log
Successfully saved container spec in flex template file.
Template File GCS Location: gs://<storage_bucket>/dataflow/flex-template/hellofruit.json
Container Spec:

{
    "defaultEnvironment": {},
    "image": "australia-southeast1-docker.pkg.dev/<project-id>/<artifact_repository_docker>/dataflow/hellofruit:0.1",
    "metadata": {
        "description": "Hello fruit Python flex template.",
        "name": "Hello fruit",
        "parameters": [
            {
                "helpText": "Name of the BigQuery output table name.",
                "isOptional": true,
                "label": "BigQuery output table name.",
                "name": "output_table",
                "regexes": [
                    "([^:]+:)?[^.]+[.].+"
                ]
            }
        ]
    },
    "sdkInfo": {
        "language": "PYTHON"
    }
}
```

### Using the gcloud CLI

This method will do the build and push as well as create the flex template JSON file. However in certain GCP setups it may not run. It is kept here for reference.

```sh
gcloud dataflow flex-template build "gs://<storage_bucket>/dataflow/flex/hellofruit.json" \
     --image-gcr-path "australia-southeast1-docker.pkg.dev/<project_id>/<artifact_repository_docker>/dataflow/hellofruit:latest" \
     --staging-location "gs://<storage_bucket>/dataflow/staging" \
     --temp-location "gs://<storage_bucket>/dataflow/temp" \
     --gcs-log-dir "gs://<storage_bucket>/dataflow/logs" \
     --sdk-language "PYTHON" \
     --flex-template-base-image "PYTHON3" \
     --metadata-file "metadata.json" \
     --py-path "." \
     --env "FLEX_TEMPLATE_PYTHON_PY_FILE=hellofruit.py" \
     --env "FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE=requirements.txt" \
     --log-http \
     --verbosity debug
```

## Logs

```log
DEBUG: Running [gcloud.dataflow.flex-template.build] with arguments: [--env: "OrderedDict([('FLEX_TEMPLATE_PYTHON_PY_FILE', 'hellofruit.py'), ('FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE', 'requirements.txt')])", --flex-template-base-image: "PYTHON3", --gcs-log-dir: "gs://<storage_bucket>/dataflow/", --image-gcr-path: "australia-southeast1-docker.pkg.dev/<project_id>/<artifact_repository_docker>/dataflow/hellofruit:latest", --log-http: "true", --metadata-file: "{
    "name": "Hello fruit",
    "description": "Hello fruit Python flex template.",
    "parameters": [
      {
        "name": "output_table",
        "label": "BigQuery output table name.",
        "helpText": "Name of the BigQuery output table name.",
        "isOptional": true,
        "regexes": [
          "([^:]+:)?[^.]+[.].+"
        ]
      }
    ]
  }", --py-path: "['.']", --sdk-language: "PYTHON", --staging-location: "gs://<storage_bucket>/dataflow/", --temp-location: "gs://<storage_bucket>/dataflow/", --verbosity: "debug", TEMPLATE_FILE_GCS_PATH: "gs://<storage_bucket>/dataflow/flex/hellofruit.json"]
Copying files to a temp directory /tmp/tmpo6flua7l
Generating dockerfile to build the flex template container image...
Generated Dockerfile. Contents: 
FROM gcr.io/dataflow-templates-base/python3-template-launcher-base:latest

ENV FLEX_TEMPLATE_PYTHON_PY_FILE=/template/hellofruit.py
ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE=/template/requirements.txt

COPY docker /template/

RUN apt-get update && apt-get install -y libffi-dev git && rm -rf /var/lib/apt/lists/* && pip install --no-cache-dir -U -r /template/requirements.txt

=======================
==== request start ====
uri: https://storage.googleapis.com/storage/v1/b/<project_id>_cloudbuild?alt=json
method: GET
== headers start ==
b'accept': b'application/json'
b'accept-encoding': b'gzip, deflate'
b'authorization': --- Token Redacted ---
b'content-length': b'0'
== headers end ==
== body start ==

== body end ==
==== request end ====
DEBUG: Starting new HTTPS connection (1): storage.googleapis.com:443
DEBUG: https://storage.googleapis.com:443 "GET /storage/v1/b/<project_id>_cloudbuild?alt=json HTTP/1.1" 404 247
---- response start ----
status: 404
-- headers start --
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Content-Length: 247
Content-Type: application/json; charset=UTF-8
Date: Thu, 07 Dec 2023 04:27:19 GMT
Expires: Mon, 01 Jan 1990 00:00:00 GMT
Pragma: no-cache
Server: UploadServer
Vary: Origin, X-Origin
-- headers end --
-- body start --
{
  "error": {
    "code": 404,
    "message": "The specified bucket does not exist.",
    "errors": [
      {
        "message": "The specified bucket does not exist.",
        "domain": "global",
        "reason": "notFound"
      }
    ]
  }
}

-- body end --
total round trip time (request+response): 0.653 secs
---- response end ----
----------------------
=======================
==== request start ====
uri: https://storage.googleapis.com/storage/v1/b?alt=json&enableObjectRetention=False&project=<project_id>
method: POST
== headers start ==
b'accept': b'application/json'
b'accept-encoding': b'gzip, deflate'
b'authorization': --- Token Redacted ---
b'content-length': b'50'
b'content-type': b'application/json'
b'x-goog-api-client': b'cred-type/u'
== headers end ==
== body start ==
{"name": "<project_id>_cloudbuild"}
== body end ==
==== request end ====
DEBUG: Starting new HTTPS connection (1): storage.googleapis.com:443
DEBUG: https://storage.googleapis.com:443 "POST /storage/v1/b?alt=json&enableObjectRetention=False&project=<project_id> HTTP/1.1" 403 546
---- response start ----
status: 403
-- headers start --
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Content-Length: 546
Content-Type: application/json; charset=UTF-8
Date: Thu, 07 Dec 2023 04:27:20 GMT
Expires: Mon, 01 Jan 1990 00:00:00 GMT
Pragma: no-cache
Server: UploadServer
Vary: Origin, X-Origin
-- headers end --
-- body start --
{
  "error": {
    "code": 403,
    "message": "<user>@<domain> does not have storage.buckets.create access to the Google Cloud project. Permission 'storage.buckets.create' denied on resource (or it may not exist).",
    "errors": [
      {
        "message": "<user>@<domain> does not have storage.buckets.create access to the Google Cloud project. Permission 'storage.buckets.create' denied on resource (or it may not exist).",
        "domain": "global",
        "reason": "forbidden"
      }
    ]
  }
}

-- body end --
total round trip time (request+response): 0.371 secs
---- response end ----
----------------------
DEBUG: (gcloud.dataflow.flex-template.build) The user is forbidden from accessing the bucket [<project_id>_cloudbuild]. Please check your organization's policy or if the user has the "serviceusage.services.use" permission. Giving the user Owner, Editor, or Viewer roles may also fix this issue. Alternatively, use the --no-source option and access your source code via a different method.

response: <
{'x-guploader-uploadid': ''
, 'content-type': 'application/json; charset=UTF-8'
, 'date': 'Thu, 07 Dec 2023 04:27:19 GMT'
, 'vary': 'Origin, X-Origin'
, 'cache-control': 'no-cache, no-store, max-age=0, must-revalidate'
, 'expires': 'Mon, 01 Jan 1990 00:00:00 GMT'
, 'pragma': 'no-cache'
, 'content-length': '247'
, 'server': 'UploadServer'
, 'status': 404
}
>
, content <
{
  "error": {
    "code": 404,
    "message": "The specified bucket does not exist.",
    "errors": [
      {
        "message": "The specified bucket does not exist.",
        "domain": "global",
        "reason": "notFound"
      }
    ]
  }
}
>


response: <
{
     'x-guploader-uploadid': ''
     , 'content-type': 'application/json; charset=UTF-8'
     , 'date': 'Thu, 07 Dec 2023 04:27:20 GMT'
     , 'vary': 'Origin, X-Origin'
     , 'cache-control': 'no-cache, no-store, max-age=0, must-revalidate'
     , 'expires': 'Mon, 01 Jan 1990 00:00:00 GMT'
     , 'pragma': 'no-cache'
     , 'content-length': '546'
     , 'server': 'UploadServer'
     , 'status': 403
}>
, content <
{
  "error": {
    "code": 403,
    "message": "<user>@<domain> does not have storage.buckets.create access to the Google Cloud project. Permission 'storage.buckets.create' denied on resource (or it may not exist).",
    "errors": [
      {
        "message": "<user>@<domain> does not have storage.buckets.create access to the Google Cloud project. Permission 'storage.buckets.create' denied on resource (or it may not exist).",
        "domain": "global",
        "reason": "forbidden"
      }
    ]
  }
}
>

googlecloudsdk.command_lib.builds.submit_util.BucketForbiddenError: The user is forbidden from accessing the bucket [<project_id>_cloudbuild]. Please check your organization's policy or if the user has the "serviceusage.services.use" permission. Giving the user Owner, Editor, or Viewer roles may also fix this issue. Alternatively, use the --no-source option and access your source code via a different method.
ERROR: (gcloud.dataflow.flex-template.build) The user is forbidden from accessing the bucket [<project_id>_cloudbuild]. Please check your organization's policy or if the user has the "serviceusage.services.use" permission. Giving the user Owner, Editor, or Viewer roles may also fix this issue. Alternatively, use the --no-source option and access your source code via a different method.
```
