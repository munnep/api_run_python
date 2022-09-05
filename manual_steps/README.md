organization name = patrickmunne
workspace name = test_api

token id = 

TOKEN=
ORG_NAME=patrickmunne
WORKSPACE_NAME=test_api
CONTENT_DIRECTORY=/Users/patrickmunne/git/api_run_python/manual_steps/example
UPLOAD_FILE_NAME="./content-$(date +%s).tar.gz"

tar -zcvf "$UPLOAD_FILE_NAME" -C "$CONTENT_DIRECTORY" .

# get the workspace id from the name
WORKSPACE_ID=($(curl \
  --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  https://app.terraform.io/api/v2/organizations/patrickmunne/workspaces/test_api \
  | jq -r '.data.id'))



curl \
  --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  https://app.terraform.io/api/v2/organizations/patrickmunne/workspaces/test_api 



# create a configuration version
echo '{"data":{"type":"configuration-versions"}}' > ./create_config_version.json

UPLOAD_URL=($(curl \
  --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  --request POST \
  --data @create_config_version.json \
  https://app.terraform.io/api/v2/workspaces/$WORKSPACE_ID/configuration-versions \
  | jq -r '.data.attributes."upload-url"'))

# upload the url
curl \
  --header "Content-Type: application/octet-stream" \
  --request PUT \
  --data-binary @"content_2022030923_06_55.tar.gz" \
  $UPLOAD_URL
