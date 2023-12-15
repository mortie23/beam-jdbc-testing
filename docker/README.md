# Dataflow build and run

Basic example of how to develop an Apache Beam pipeline and build and deploy it as a Dataflow job.
This example avoids complexities of reading from source systems or storage and simply creates synthetic data.
It then writes the data to a BigQuery table.

Working from these examples: 

- [Using Flex Templates](https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates#local-shell)
- [streaming_beam.py](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/dataflow/flex-templates/streaming_beam/streaming_beam.py)

## Setup

### Project

Firstly the basic project naming convention we will have will include an environment.

```
prj-<org>-<env>-<business-unit>
```

In this example, the Organisation is **XYZ**, and the Business unit is **Fruit**

The project requires:

- GCP Artifact registry 
  - Docker repository
- DataFlow API
- Cloud storage
- BigQuery

### IAM

- Service account with roles
  - Artifact Registry Repository Administrator
  - Storage Object Admin
  - Dataflow Worker
  - Workflows Invoker
  - BigQuery custom role (permissions)
    - bigquery.tables.create
    - bigquery.tables.get
    - bigquery.tables.update
    - bigquery.tables.updateData

### Cloud storage 

Cloud storage bucket with sub folders

```
📁 dataflow/
│   ├── 📁 flex-template/
│   ├── 📁 staging/
│   ├── 📁 logs/
│   ├── 📁 temp/
```

### BigQuery

Make sure the target table within the appropriate dataset exists.

```sql
create table fruit.hellofruit (
  name string
  , test_number int64
)
```

## Build

The build step involves building a Docker container image, and associated Flex template file.

[README build](README-build.md)

## Run

Running a Dataflow job using a built flex template and Docker container

[README run](README-run.md)

## Notes

This documents the extra steps of building the Docker image locally and pushing it to a container registry that can be required depending on your setup in GCP.
The recommended `gcloud dataflow flex-template build` command uses Cloud build which will need to create a Storage bucket with the naming convention `<project_id>_cloudbuild` within the US region.
You may get something like the following:

```log
DEBUG: Starting new HTTPS connection (1): storage.googleapis.com:443
DEBUG: https://storage.googleapis.com:443 "GET /storage/v1/b/<project_id>_cloudbuild?alt=json HTTP/1.1" 404 247
```
```json
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
```

Reasons could include:

- maybe you have a restricted VPC that does not allow services outside a particular region
- maybe the access granted to you as a _Data Engineer_ does not allow for _Storage bucket_ creation
