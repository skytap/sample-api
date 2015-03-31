#!/usr/bin/env python

'''
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
Python script to HTTP PUT to the Skytap API to start up a specific
VM in a an existing Configuration/Environment, which is done by changing the
runstate to running (by PUTting a change to the VM resource).
This is a very simple python script to serve as an example
for beginner to get started making API calls to Skytap.

NOTE: Throughout the Skytap API, environments are referred to as "configurations."
      Skytap no longer uses the term "configurations" in the web interface; however,
      it has been maintained in the API for backwards-compatibility.

This code was tested with python 2.7.5

'''

import requests
import json

# Define the requesite headers and authorization for the Skytap API
auth = ('username', 'password')      # login and API token/password
# Requisite JSON headers for API
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# URL below PUTs a change to the VM ID 1234567 to start it up
# VM ID 1234567 is contained in the Environment with ID 1234321
url = 'https://cloud.skytap.com/configurations/1234321/vms/1234567'
params = {'runstate': 'running'}

# PUT and print the results
result = requests.put(url, headers=headers, auth=auth, params=params)
print("status_code = %s" % result.status_code)

# Next two lines make the json response pretty
json_output = json.loads(result.text)
print(json.dumps(json_output, indent=4))

# Note: the VM resource will be in a busy, locked state until the VM is started
