import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
CLEARSCAPE_TOKEN = os.getenv("CLEARSCAPE_TOKEN")

# Define the API endpoint URL
url = "https://api.clearscape.teradata.com/environments"

# Create headers with the Bearer token
headers = {"Authorization": f"Bearer {CLEARSCAPE_TOKEN}"}

# Make the GET request with the headers
response = requests.get(url, headers=headers)

# Check the response status code
if response.status_code == 200:
    # The request was successful
    data = response.json()  # If the response contains JSON data
    print("Response data:")
    print(json.dumps(data, indent=2))
else:
    # Request failed
    print(f"Request failed with status code: {response.status_code}")
    print("Response content:")
    print(response.text)
