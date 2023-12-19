from google.cloud import secretmanager


def access_secret(project_id, secret_id, version_id=1):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


PROJECT_ID = "prj-xyz-dev-fruit"
SECRET_ID = "teradata_clearscape_password"
secret_value = access_secret(project_id=PROJECT_ID, secret_id=SECRET_ID)
print("Secret value:", secret_value)
