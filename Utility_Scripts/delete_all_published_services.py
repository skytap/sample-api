#!/usr/bin/env python

"""

    delete_all_published_services.py

    Sample script using Skytap API. From global list of users, compiles a list of Skytap Configurations and
    then deletes ALL Published Services for each Configuration.

    When completed, provides a summary of the number (if any) of Published Services deleted for each user.  The user 
    is listed by email address - script may be modified to email admin of the Published Service security violation.

    Note:  Requires Skytap Admin API login to obtain the list of all users

    tested with python v3.4.1
    last updated 9/8/2014, FP

"""

import requests
import json
import sys
import logging
import time

logging.basicConfig(filename='skytap_delete_published_services.log', level=logging.INFO)

### Default values  ###
user_credentials = ('username', 'password')  # add credentials here


# -----subroutine definitions----

def fib():
    """  Generator for fibonacci sequence.  Intended for use in waiting between
         API calls when retrying busy operations."""

    a, b = 1, 2  # starts with 1, no need to sleep 0 seconds on first run
    while 1:
        yield a
        a, b = b, a + b


def delete_all_published_services(user_credentials, config_id):
    """
        Loop through ALL VM's interfaces in a configuration and delete Published Services for each interface.
        Returns a count of the number of Published Services deleted
    """

    config_url = 'https://cloud.skytap.com/configurations/' + str(config_id)
    resp = requests.get(config_url, auth=user_credentials, headers=headers)
    config_json = json.loads(resp.text) 
    num_services = 0

    if config_json["vms"]:   # prevents breaking config with no VMs (corner case)
        for vm in config_json["vms"]:
            vm_id = vm["id"]
            for interface in vm["interfaces"]:
                interface_id = interface["id"]
                for service in interface["services"]:
                    num_services += 1
                    port_num = service["id"]
                    url = config_url + '/vms/' + vm_id + '/interfaces/' + interface_id + '/services/' + port_num
                    pubservice_delete_resp = requests.delete(url, headers=headers, auth=user_credentials)
                    if pubservice_delete_resp.status_code == 200:
                        print("Successfully Deleted Published Service: " + str(port_num) + " on: " + str(interface_id))
                    elif (pubservice_delete_resp.status_code == 422 or pubservice_delete_resp.status_code == 423
                          or pubservice_delete_resp.status_code == 409):
                        fib_wait = fib()
                        total_seconds = 0
                        max_seconds = 120  # roughly 2 minutes
                        while total_seconds < max_seconds:
                            fibnum = next(fib_wait)
                            time.sleep(fibnum)
                            print("VM busy - cannot delete Published Service.  Retrying.")
                            total_seconds += fibnum
                            try:
                                pubservice_delete_resp = requests.delete(url, headers=headers, auth=user_credentials)
                            except requests.exceptions.ConnectionError: 
                                logging.info("Network unstable or not connected, exception handled, retrying...")
                                pass  # if run from within a VM, can cause the network interface to bounce; ignore it
                            if pubservice_delete_resp.status_code == 200:
                                print("Successfully Deleted Published Service: " + str(port_num) + " on: "
                                      + str(interface_id) + " after retry.")
                                break
                        if not (pubservice_delete_resp.status_code == 200):
                            print("Failed Deleting Pub Service: " + str(port_num) + "  on: " + str(interface_id))
                            logging.info("Failed Deleting Pub Service: " + str(port_num) + "  on: " + str(interface_id))
                            logging.info("API returned Status Code: " + str(pubservice_delete_resp.status_code))
                            logging.info(pubservice_delete_resp.text)
                    else:
                        print("Failed Deleting Published Service: " + str(port_num) + "  on: " + str(interface_id))
                        logging.info("Failed Deleting Published Service: " + str(port_num) + "  on: "
                                     + str(interface_id))
                        logging.info("API returned Status Code: " + str(pubservice_delete_resp.status_code))
                        logging.info(pubservice_delete_resp.text)
                    time.sleep(1) 
    return num_services

# Run program ---------------------------------------------------------------------------------------------------------

if user_credentials[0] == "username":
    print("User Credentials not set, aborting program")
    sys.exit(1)

config_count = 0
total_published_services_count = 0

# For Skytap API (even for an admin user), there is no method to get list of all Configuration
# as a workaround, we get list of all users, then process all their Configurations
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
users_url = 'https://cloud.skytap.com/users/'
resp = requests.get(users_url, auth=user_credentials, headers=headers)  # gets the list of all users
logging.info("API Response getting user list: " + resp.text)
user_list_json = json.loads(resp.text)

for user in user_list_json:
    published_services_found = 0
    resp = requests.get(user["url"], auth=user_credentials, headers=headers)
    user_details_json = json.loads(resp.text)

    for config in user_details_json["configurations"]:    # get the list of Configurations for a user
        resp = requests.get(config["url"], auth=user_credentials, headers=headers)
        config_details_json = json.loads(resp.text)
        published_services_found += delete_all_published_services(user_credentials, config_details_json["id"])
        config_count += 1
    if published_services_found > 0:
        #  if published services found, print and log the number deleted and the offending user's email address
        print(" Security policy violated with user with the email address:  " + user_details_json["email"]
              + " --> " + str(published_services_found) + " Published Services Found!")
        logging.info("!Security policy violated with user with the email address: " + user_details_json["email"]
                     + " --> " + str(published_services_found) + " Published Services Found!")
    total_published_services_count += published_services_found

print("Processed " + str(config_count) + " Configurations.")
logging.info("Processed " + str(config_count) + " Configurations.")
print("Deleted " + str(total_published_services_count) + " Published Services.")
logging.info("Deleted " + str(total_published_services_count) + " Published Services.")
