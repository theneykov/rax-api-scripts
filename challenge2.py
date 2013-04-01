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
Challenge 2:
Write a script that clones a server
(takes an image and deploys the image as a new server).
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
    print("Did you remember to replace the credential file with your actual" +
          " username and api_key?")

if pyrax.identity.authenticated:
    print("Successfully authenticated.")
else:
    print("Authentication failed. Exiting...")
    sys.exit(1)

print("Preparing to clone server...")
cs = pyrax.cloudservers

server_matrix = []
print("Servers in current region:")
srv_count = 0
for srv in cs.servers.list():
    srv_count += 1
    # print str(srv_count) + ") " + srv.id + " " + srv.name
    # add entry to matrix so user can select server number later to image
    server_matrix.append([srv_count, str(srv.id), str(srv.name)])

if srv_count == 0:
    print("You don't have any NextGen servers in this region to create an" +
          " image from.")
    print("Can't continue. Exiting...")
    sys.exit(1)

# print("Server list:"
print("")
for s in server_matrix:
    print(str(s[0]) + ") " + s[1] + " " + s[2])

print("")
print("Please enter the number of the server you wish to clone:"),
srv_num = raw_input()
try:
    srv_num = int(srv_num)
except:
    print("Value must be an integer. Exiting.")
    sys.exit(1)

# srv_num = int(srv_num)
if srv_num > srv_count or srv_num <= 0:
    print("Error specifying server number: Outside of range. Exiting.")
    sys.exit(1)

print("Please enter the name of the new image you wish to create:"),
new_image_name = raw_input()
new_image_name = new_image_name.strip()

print("Please enter the name of the new server to be created:"),
new_server = raw_input()
new_server = new_server.strip()

for c in server_matrix:
    if int(c[0]) == srv_num:
        print("")
        print("Creating image '" + new_image_name + "' of server '" + c[2] +
              "' (" + c[1] + ") .")
        img_uuid = cs.servers.create_image(c[1], new_image_name)

print("Saving image '" + new_image_name + "' with uuid=" + str(img_uuid))
img_active = False
while not img_active:
    time.sleep(60)
    for img in cs.images.list():
        if img.id == img_uuid:
            if img.status == "ACTIVE":
                img_active = True
                print("Image was saved.")
                print("")
            else:
                print("Image is still saving. Sleeping 60 seconds." +
                      " Progress: " + str(img.progress) + "%")

# Create server from image img_id
server_matrix = []
print("Creating server '" + new_server + "' from image '" +
      new_image_name + "'.")
try:
    server = cs.servers.create(new_server, img_uuid, "2")
    server_matrix.append([str(server.id), str(server.name),
                          str(server.adminPass), ""])
except:
    print("Failed to build server from image.")

received_ips = False
while not received_ips:
    print("Waiting for server to fully provision. Sleeping for 30 seconds.")
    time.sleep(30)
    print("")
    received_ips = True
    # get server list and populate server_matrix with IPs
    for y in cs.servers.list():
        index = 0
        for s in server_matrix:
            if y.id == server_matrix[index][0]:
                # print i.networks
                for k, v in y.networks.iteritems():
                    if k == "public":
                        if len(v[0]) > 15:
                            # print v[1]
                            server_matrix[index][3] = str(v[1])
                        else:
                            # print v[0]
                            server_matrix[index][3] = str(v[0])
            index += 1
    for x in server_matrix:
        # print(x)
        if len(x[3]) < 1:
            received_ips = False
print("")
print("['                uuid                ', ' name ', " +
      "'root password', 'IP address']")
for x in server_matrix:
    print(x)
