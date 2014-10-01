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

 delete_all_published_sets.py

Sample script using Skytap API. From global list of users, compiles a list of Skytap Configurations and
then deletes ALL Published Sets (aka, Published URLs) for each Configuration.

When completed, provides a summary of the number (if any) of Published Sets deleted for each user.  The user
is listed by email address - script may be modified to email administrator of the security violation.

Note:  Requires Skytap Administrator API login to obtain the list of all users

Tested with Python 3.4.1  (not compatible with Python 2)
v1.0

"""

import requests
import json
import sys
import logging
import time

logging.basicConfig(filename='skytap_delete_published_sets.log', level=logging.INFO)

### Default values  ###
user_credentials = ('username', 'password')  # add credentials here


# -----subroutine definitions----

def delete_all_published_sets(user_credentials, config_id):
    """
        Loop through ALL VM's interfaces in a configuration and deletes Published Sets (aka Published URLs)
        Returns a count of the number of Published URLs deleted
    """
    num_publish_sets_deleted = 0

    pub_set_url = 'https://cloud.skytap.com/configurations/' + config_id + '/publish_sets/'
    resp = requests.get(pub_set_url, auth=user_credentials, headers=headers)
    pub_set_details_json = json.loads(resp.text)

    for pub_set in pub_set_details_json:
        delete_url = 'https://cloud.skytap.com/configurations/' + config_id + '/publish_sets/' + pub_set["id"]
        pubset_delete_resp = requests.delete(delete_url, headers=headers, auth=user_credentials)

        if pubset_delete_resp.status_code == 200:
            print("Successfully Deleted Publish Set: " + str(pub_set["id"]))
            num_publish_sets_deleted += 1
        else:
            print("Failed Deleting Publish Set: " + str(pub_set["id"]))
            logging.info("Failed Deleting Published Set: " + str(pub_set["id"]))
            logging.info(pubset_delete_resp.text)
        time.sleep(1)  # slow it down a bit

    return num_publish_sets_deleted

# Run program ---------------------------------------------------------------------------------------------------------

if user_credentials[0] == "username":
    print("User Credentials not set, aborting program")
    sys.exit(1)

config_count = 0
total_published_sets_count = 0

# For Skytap API (even for an admin user), there is no method to get list of all Configuration
# as a workaround, we get list of all users, then process all their Configurations
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
users_url = 'https://cloud.skytap.com/users/'
resp = requests.get(users_url, auth=user_credentials, headers=headers)  # gets the list of all users
logging.info("API Response getting user list: " + resp.text)
user_list_json = json.loads(resp.text)

for user in user_list_json:
    published_sets_found = 0
    resp = requests.get(user["url"], auth=user_credentials, headers=headers)
    user_details_json = json.loads(resp.text)

    for config in user_details_json["configurations"]:    # get the list of Configurations for a user
        resp = requests.get(config["url"], auth=user_credentials, headers=headers)
        config_details_json = json.loads(resp.text)
        published_sets_found += delete_all_published_sets(user_credentials, config_details_json["id"])
        config_count += 1
    if published_sets_found > 0:
        #  if published sets found, print and log the number deleted and the offending user's email address
        print(" Security policy violated with user with the email address:  " + user_details_json["email"]
              + " --> " + str(published_sets_found) + " Published Sets Found!")
        logging.info("!Security policy violated with user with the email address: " + user_details_json["email"]
                     + " --> " + str(published_sets_found) + " Published Sets Found!")
    total_published_sets_count += published_sets_found

print("Processed " + str(config_count) + " Configurations.")
logging.info("Processed " + str(config_count) + " Configurations.")
print("Deleted " + str(total_published_sets_count) + " Published Sets.")
logging.info("Deleted " + str(total_published_sets_count) + " Published Sets.")


