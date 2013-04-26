#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2013 Ted Neykov

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Challenge 13:
Write an application that nukes everything in your Cloud Account. It should:
- Delete all Cloud Servers
- Delete all Custom Images
- Delete all Cloud Files Containers and Objects
- Delete all Databases
- Delete all Networks
- Delete all CBS Volumes
"""

import os
import sys
import string
import pyrax
import pyrax.exceptions as exc
import time

print("Using credentials file: ~/.rackspace_cloud_credentials")
cred_file = os.path.expanduser("~/.rackspace_cloud_credentials")
#print("Using credentials file: ~/.rackspace_DELETE_ALL_THE_THINGS")
#cred_file = os.path.expanduser("~/.rackspace_DELETE_ALL_THE_THINGS")
try:
    pyrax.set_credential_file(cred_file)
except exc.AuthenticationFailed:
    print("Did you remember to replace the credential file with your actual" +
          "username and api_key?")

if pyrax.identity.authenticated:
    print("Successfully authenticated.")
else:
    print("Authentication failed. Exiting...")
    sys.exit(1)


def delete_all_clb():
    print("Deleting all Cloud Load Balancers...")
    clb = pyrax.cloud_loadbalancers
    for lb in clb.list():
        print("...deleting: " + str(lb.id) + " " + str(lb.name))
        lb.delete()
    print("Done.")


def delete_all_dbaas():
    print("Deleting all Cloud Database Instances...")
    cdb = pyrax.cloud_databases
    for db in cdb.list():
        print("...deleting: " + str(db.id) + " " + str(db.name))
    print("Done.")


def delete_all_servers():
    pass


def delete_all_cbs():
    pass


def delete_all_images():
    pass


def delete_all_cf():
    pass

print("\n!!! THIS WILL DELETE EVERYTHING FROM THE ACCOUNT !!!")
destroy = raw_input("Are you sure? Type 'Yes' to proceed: ")

if destroy == "Yes":
    delete_all_clb()
    delete_all_dbaas()
    delete_all_servers()
    delete_all_cbs()
    delete_all_images()
    delete_all_cf()
else:
    print("Exiting. Nothing was changed or deleted.")
