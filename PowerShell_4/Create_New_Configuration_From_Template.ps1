<#
Copyright 2014 Skytap Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#-----------------------------------------------------------------------
# Example Powershell script for Creating a new Configuration from Template using the Skytap API.
#>

#Skytap credentials 
$username = <your_skytap_login_id>
$password = <your_login_or_API_Token>

#convert username:password for basic Authentication with Skytap API
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f $username,$password)))

#set base URI for the Skytap resource you are accessing.  In this example, Configurations.
$uri = "https://cloud.skytap.com/configurations"

#set requisite headers for Skytap API (JSON preferred, could use xml as well)
$headers = @{"Accept" = "application/json"; Authorization=("Basic {0}" -f $base64AuthInfo)}

#external template.json file specifies from which Template to create new config - edit this use your desired Template_ID
#Make the API Call to POST Template ID to Configurations resource (to Create new config from Template)
Invoke-RestMethod -Uri $uri -Method POST -Body (Get-Content template.json -Raw) -ContentType "application/json" -Headers $headers
