#!/usr/bin/env python

'''get_configuration.py

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

#------------------------------------------------------------------------
A simple python script for a GET to the Skytap API to list  the Environments/Configurations in a user's Skytap
account in the json format. This is a very simple python script to serve as an example for beginner to get started
making API calls to Skytap.
NOTE: Throughout the Skytap API, environments are referred to as "configurations." Skytap no longer uses the term
      "configurations" in the web interface; however, it has been maintained in the API for backwards-compatibility.

This code was tested with python 2.7.5

'''

import requests 
import json

## define the requesite url, headers, and authorization for the Skytap API ##
url = 'https://cloud.skytap.com/configurations' # base URL for configurations
auth = ('username', 'password')                 # login and password/API Token
headers = { 'Accept': 'application/json', 'Content-type': 'application/json'}

## GET and print the results ##
api_response = requests.get(url, headers=headers, auth=auth)
print("HTTP status_code = %s" % api_response.status_code)
# next two lines make the json response pretty
json_output = json.loads(api_response.text)
print json.dumps(json_output, indent = 4)
