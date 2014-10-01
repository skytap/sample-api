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

 import_users_from_csv.py

Example python script for performing a bulk creation of users in Skytap.
Expects input of a csv file with specific fields for user and quota information.
Requires Adminstrator (or User Manager) credentials in Skytap.
Prompts user for all inputs values.

Tested with Python 3.4.1  (not compatible with Python 2)
v1.2

"""

import csv
import sys
import json
import requests  # can be installed via pip

# get username, API Token/password, and csv filename from user input
userid = input('\nPlease enter your Skytap ADMINISTRATOR login: ')
passwd = input('Please enter your Skytap API Token or password: ')
csv_filename = input('Please enter the name of your csv file to be processed: ')

# loop through csv file, creating users and adding quotas per csv file 
with open(csv_filename, 'rU') as csvfile:
    user_reader = csv.reader(csvfile, delimiter=',', quotechar='"')

    for row in user_reader:
        (firstname, lastname, title, role, login, email, tz, can_export,
         can_import, pub_lib, concurrent_vms, concurrent_storage_size, concurrent_svms,
         cumulative_svms) = row

        if login == 'sample_user' and email == 'email':
            next(user_reader)  # skip the header line (assumption given that it matches the user_test.csv sample file)

        # setup data to add new user using details provided in csv file to send to API
        url = 'https://cloud.skytap.com/users/'
        auth = (userid, passwd)
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        userdata = {
            "first_name": firstname,
            "last_name": lastname,
            "title": title,
            "account_role": role,
            "login_name": login,
            "email": email,
            "time_zone": tz,
            "can_export": can_export,
            "can_import": can_import,
            "has_public_library": pub_lib
        }

        # call to API to add new user using details provided in csv file 
        api_response = requests.post(url, headers=headers, auth=auth, params=userdata)
        if 'Invalid credentials' in api_response.text:
            print("Invalid Credentials.  Please Try again. ")
            sys.exit()
        elif api_response.status_code == 200:
            print("Successfully added user with the login: " + login)
            jsout = json.loads(api_response.text)
            user_quota_url = jsout["url"] + '/quotas'

            ## Adding quotas for users (in next four blocks)
            url = user_quota_url + '/' + 'concurrent_storage_size'
            params = {"limit": str(concurrent_storage_size)}
            api_response = requests.put(url, headers=headers, auth=auth, params=params)
            if api_response.status_code == 200:
                print("\tSuccessfully added concurrent storage size quota for the login: " + login)
            else:
                print(api_response.text)

            # Set Concurrent SVM quota 
            url = user_quota_url + '/' + 'concurrent_svms'
            params = {"limit": str(concurrent_svms)}
            api_response = requests.put(url, headers=headers, auth=auth, params=params)
            if api_response.status_code == 200:
                print("\tSuccessfully added concurrent svms quota for the login: " + login)
            else:
                print(api_response.text)

            # Set Concurrent VM quota 
            url = user_quota_url + '/' + 'concurrent_vms'
            params = {"limit": str(concurrent_vms)}
            api_response = requests.put(url, headers=headers, auth=auth, params=params)
            if api_response.status_code == 200:
                print("\tSuccessfully added concurrent vms quota for the login: " + login)
            else:
                print(api_response.text)

            # Set Cumulative SVM quota 
            url = user_quota_url + '/' + 'cumulative_svms'
            params = {"limit": str(cumulative_svms)}
            api_response = requests.put(url, headers=headers, auth=auth, params=params)
            if api_response.status_code == 200:
                print("\tSuccessfully added cumulative svms quota for the login: " + login)
            else:
                print(api_response.text)
        else:
            print("\nUnable to add the user with login: " + login)
            print("Error from API: " + api_response.text)
            print("User skipped, moving to next user")
