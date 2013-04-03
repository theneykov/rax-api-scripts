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
Challenge 5:
Write a script that creates a Cloud Database instance. 
This instance should contain at least one database, 
and the database should have at least one user that can connect to it.
"""

import os
import sys
import string
import pyrax
import pyrax.exceptions as exc
import time

print("Using credentials file: ~/.rackspace_cloud_credentials")
cred_file = os.path.expanduser("~/.rackspace_cloud_credentials")
try:
    pyrax.set_credential_file(cred_file)
except exc.AuthenticationFailed:
    print("Did you remember to replace the credential file with your actual",
          "username and api_key?")

if pyrax.identity.authenticated:
    print("Successfully authenticated.")
else:
    print("Authentication failed. Exiting...")
    sys.exit(1)

cdb = pyrax.cloud_databases

print("Please enter a name for the new DBaaS instance you're aboout to create:"),
db_inst_name = raw_input()
db_inst_name = db_inst_name.strip()

print("Please enter a name for the new database within the instance:"),
db_db_name = raw_input()
db_db_name = db_db_name.strip()

print("Please enter the username for the database:"),
db_db_user = raw_input()
db_db_user = db_db_user.strip()

print("Please enter the password for " + db_db_user + ":"),
db_db_pass = raw_input()
db_db_pass = db_db_pass.strip()

print("Please enter the size of the disk volume for the DBaaS instance (in GB):"),
db_vol = raw_input()
try:
    db_vol = int(db_vol)
except ValueError:
    print("Disk volume value must be an integer between 1 and 150. Exiting...")
    sys.exit(1)

if db_vol < 1 or db_vol > 150:
    print("Disk volume value must be an integer between 1 and 150. Exiting...")
    sys.exit(1)

print("ID Flavor Name   RAM")
flv_index = 0
for flv in cdb.list_flavors():
    flv_index += 1
    print(str(flv.id) + " " + str(flv.name) + " " + str(flv.ram))

print("From the list above, please select a flavor ID:"),
db_flv = raw_input()
try:
    db_flv = int(db_flv)
except:
    print("ID entered must be an integer ID from the list above. Exiting...")
    sys.exit(1)

if db_flv < 1 or db_flv > flv_index:
    print("ID is out of range. Exiting...")
    sys.exit(1)

print("Creating DBaaS instance '" + db_inst_name + "'...")

db_inst = cdb.create(db_inst_name, flavor=db_flv, volume=db_vol)

"""
print(db_inst.name)
print(db_inst.id)
print(db_inst.hostname)
print(db_inst.status)
"""

db_built = False
while not db_built:
    db_instances = cdb.list()
    for dbs in db_instances:
        if str(dbs.id) == str(db_inst.id):
            if str(dbs.status) == "ACTIVE":
                db_built = True
            else:
                print("DBaaS instance is still building...Sleeping 30 seconds.")
                time.sleep(30)
        
print("Creating database...")
db = db_inst.create_database(db_db_name)
print("Creating user...")
user = db_inst.create_user(name=db_db_user, password=db_db_pass, database_names=[db_db_name])
print("Done")
print("")
print("You can connect to the database using the following command:")
print("mysql -u " + db_db_user + " -p -h " + str(db_inst.hostname))
print("")
