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

A Python script to POST of a json file to the Skytap API
to add a new schedule to an existing configuration.
This is a very simple python script to serve as an example
for beginner to get started making API calls to Skytap.

This code was tested with python 2.7.5

Note: requires the requests python module which is
open source (Apache2 licensed) and can be installed via Pip
'''

import requests
import json

## define the requesite url, headers, and authorization for the Skytap API ##
url = 'https://cloud.skytap.com/schedules'    #base URL for configurations
auth = ( 'username', 'password' )             #login and password/API Token
headers = { 'Accept' : 'application/json',     #requesite json headers for API
            'Content-Type' : 'application/json',
            'charset' : 'utf-8'
}
json_file = open('new_schedule.json', 'r')      #open the file new_schedule.json

## POST and print the results ##
result = requests.post(url, headers=headers, auth=auth, data=json_file)
print
print "status_code = %s" % result.status_code
print
json_out = json.loads(result.text)
print json.dumps(json_out, indent=5)



