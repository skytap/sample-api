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
to add a new schedule to an existing Configuration/Environment.
This is a very simple python script to serve as an example
for beginner to get started making API calls to Skytap.

NOTE: Throughout the Skytap API, environments are referred to as "configurations."
      Skytap no longer uses the term "configurations" in the web interface; however,
      it has been maintained in the API for backwards-compatibility.

This code was tested with python 2.7.5
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
print("status_code = %s" % result.status_code)
json_out = json.loads(result.text)
print(json.dumps(json_out, indent=5))



