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
VM in a an existing configuration, which is done by changing the
runstate to running (by PUTting a change to the VM resource).
This is a very simple python script to serve as an example
for beginner to get started making API calls to Skytap.

This code was tested with python 2.7.5

Note: requires the requests python module which is
open source (Apache2 licensed) and can be installed via Pip
'''

import requests
import json

## define the requesite headers and authorization for the Skytap API ##
auth = ( 'username', 'password' )               #login and password/API Token
headers = {                                      #requesite json headers for API
           'Accept' : 'application/json',
           'Content-Type' : 'application/json'
}

## URL below PUTs a change to the VM ID 1234567 to start it up ##
url = 'https://cloud.skytap.com/vms/1234567'
params = {'runstate' : 'running'}

## PUT and print the results ##
result = requests.put(url, headers=headers, auth=auth, params=params)
print
print "status_code = %s" % result.status_code
print
# next two lines make the json response pretty
json_output = json.loads(result.text)
print json.dumps(json_output, indent = 4)

# Note: the VM resource will be in a busy, locked state until the VM is started #
