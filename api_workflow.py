import argparse
import os
from datetime import datetime
import tarfile
import requests
import json

# Check that you have a Token set in your environment
token = os.environ.get('TOKEN')
if token == None:
    print("please set TOKEN environment")
    print("example: export TOKEN=hsadlkfbaskbkhbsdvkhsdbvksdhv")
    exit()


# The arguments that need to be specified
parser = argparse.ArgumentParser()
parser.add_argument("organization", help="name of the organization", type=str)
parser.add_argument("workspace", help="name of the workspace", type=str)
parser.add_argument("content_directory", help="path of the directory to zip and upload", type=str)
args = parser.parse_args()

organization = args.organization
workspace = args.workspace
content_directory = args.content_directory

# Create a unique tar.gz with the configuration files to upload
upload = "content_" + datetime.now().strftime("%Y%m%d_%H_%M_%S")

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename + ".tar.gz", "w:gz") as tar:
        tar.add(source_dir, arcname="./")
        
make_tarfile(upload, content_directory)

# get the workspace ID 
headers = {
    'Authorization': f"Bearer {token}",
    'Content-Type': 'application/vnd.api+json',
}

workspace_url = "https://app.terraform.io/api/v2/organizations/" + organization + "/workspaces/" + workspace
response = requests.get(workspace_url, headers=headers)
data = response.json()
workspace_id = (data["data"]["id"])

# create a configuration version
upload_url_data = {"data":{"type":"configuration-versions"}}

# get the upload url
upload_url = "https://app.terraform.io/api/v2/workspaces/" + workspace_id + "/configuration-versions"
response2 = requests.post(upload_url, headers=headers, json=upload_url_data)

data2 = response2.json()
upload_url_result = (data2["data"]["attributes"]["upload-url"])

# upload the tar.gz file to the upload url
headers = {
    'Content-Type': 'application/octet-stream',
}

with open(upload + ".tar.gz", 'rb') as f:
    data = f.read()

response = requests.put(upload_url_result, headers=headers, data=data)

# remove the tar.gz file 
os.remove(upload + ".tar.gz")

print("upload done")