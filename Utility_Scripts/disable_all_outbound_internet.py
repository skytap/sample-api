#!/usr/bin/env python

"""
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

-----------------------------------------------------------------------

 disable_all_outbound_internet.py

Sample script using Skytap API. From global list of Skytap Users, compiles a list of Skytap configurations
and disables outbound Internet Access for ALL Configurations in an account. Requires Skytap Admin API login to
obtain the list of all users.

When completed, provides a summary of the number (if any) of Configurations which had outbound Internet Access
enabled (presumably) by a user.  The user is listed by email address - script may be modified to email
administrator of the Published Service security violation.

NOTE: Throughout the Skytap API, environments are referred to as "configurations." Skytap no longer uses the term
      "configurations" in the web interface; however, it has been maintained in the API for backwards-compatibility.

Tested with Python 3.4.1  (not compatible with Python 2)
v1.0

"""

import requests
import json
import sys
import logging

logging.basicConfig(filename='disable_skytap_outbound_internet.log', level=logging.INFO)

### Default values  ###
user_credentials = ('username', 'password')  # add credentials here

if user_credentials[0] == "username":
    print("User Credentials not set, aborting program")
    sys.exit(1)

config_count = 0
total_internet_outbound_access_violation_count = 0

# For Skytap API (even for an admin user), there is no method to get list of all Configurations
# as a workaround, we get list of all users, then process all their Configurations
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
users_url = 'https://cloud.skytap.com/users/'
resp = requests.get(users_url, auth=user_credentials, headers=headers)  # gets the list of all users
logging.info("API HTTP Response getting user list: " + str(resp.status_code))
user_list_json = json.loads(resp.text)

for user in user_list_json:
    internet_access_enabled_violation_found = 0
    resp = requests.get(user["url"], auth=user_credentials, headers=headers)
    user_details_json = json.loads(resp.text)

    for config in user_details_json["configurations"]:    # get the list of Configurations for a user
        resp = requests.get(config["url"], auth=user_credentials, headers=headers)
        config_details_json = json.loads(resp.text)
        if config_details_json["disable_internet"] == 0:
            internet_access_enabled_violation_found += 1
            params = {"disable_internet": "true"}
            resp = requests.put(config["url"], auth=user_credentials, headers=headers, params=params)
            logging.info("For Configuration ID: " + config_details_json["id"] + ", response from PUT to API to disable "
                         + "outbound Internet: " + str(resp.status_code))
        config_count += 1
    if internet_access_enabled_violation_found > 0:
        #  if outbound internet access enabled found, print and log the number deleted and the offending user's email
        print(" Security policy violated by user with the email address:  " + user_details_json["email"]
              + " --> " + str(internet_access_enabled_violation_found) + " Configuration(s) with Outbound "
              + " Internet Access enabled!")
        logging.info(" Security policy violated by user with the email address:  " + user_details_json["email"]
                     + " --> " + str(internet_access_enabled_violation_found) + " Configuration(s) with Outbound "
                     + " Internet Access enabled!")
    total_internet_outbound_access_violation_count += internet_access_enabled_violation_found


print("Successfully Processed " + str(config_count) + " Configurations.")
logging.info("Successfully Processed " + str(config_count) + " Configurations.")
print("Disabled Internet Access on " + str(total_internet_outbound_access_violation_count) + " Configurations.")
logging.info("Disabled Internet Access on " + str(total_internet_outbound_access_violation_count) + " Configurations.")
