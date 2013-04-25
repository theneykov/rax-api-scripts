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
Challenge 10:
- Create 2 servers, supplying a ssh key to be installed at 
  /root/.ssh/authorized_keys.
- Create a load balancer
- Add the 2 new servers to the LB
- Set up LB monitor and custom error page.
- Create a DNS record based on a FQDN for the LB VIP.
- Write the error page html to a file in cloud files for backup.
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
          "username and api_key?")

if pyrax.identity.authenticated:
    print("Successfully authenticated.")
else:
    print("Authentication failed. Exiting...")
    sys.exit(1)

# variable to hold the count of how many servers will be built
srv_count = 2
srv_img = "e4dbdba7-b2a4-4ee5-8e8f-4595b6d694ce" # Ubuntu 12.04 LTS (Precise Pangolin)"
srv_flv = 2

print("You are about to create " + str(srv_count) + 
      " 512MB Ubuntu 12.04 LTS Cloud Servers.")
print("Please enter the servers' base name (ie. type: web to create servers" +
      "web1, web2, web3, ...)")
print("Base name:"),
cs_base_name = raw_input()

print("Server names will be:")
for i in range(1, srv_count + 1):
    print(cs_base_name + str(i))

ssh_key_location = raw_input("Enter the location of the ssh key file: ")
if not os.path.exists(ssh_key_location):
    print(ssh_key_location +": No such file or directory. Exiting...")
    sys.exit(1)
else:
    with open(ssh_key_location, 'r') as f:
        ssh_key = f.read()

# Build dicst for injecting ssh key
files = {"/root/.ssh/authorized_keys": ssh_key} 

answer = raw_input("Proceed with creating server instances? y/n: ")

if answer == "y":
    cs = pyrax.cloudservers
    server_matrix = []

    for s in range(1, srv_count + 1):
        current_name = cs_base_name + str(s)
        print("Creating server: " + current_name)
        # Create server:
        server = cs.servers.create(current_name, srv_img, srv_flv, files=files)
        # Add server information to matrix
        server_matrix.append([str(server.id), str(server.name),
                              str(server.adminPass), ""])
    print("Servers are building...waiting to obtain IP information.")
    received_ips = False
    count_done = 0
    while not received_ips:
        print("Not all IPs have been assigned. (" + str(count_done) + "/" +
              str(srv_count) + ") Sleeping for 30 seconds.")
        time.sleep(30)
        received_ips = True
        # get server list and populate server_matrix with IPs
        for y in cs.servers.list():
            index = 0
            for s in server_matrix:
                if y.id == server_matrix[index][0]:
                    # print(i.networks
                    for k, v in y.networks.iteritems():
                        if k == "public":
                            if len(v[0]) > 15:
                                # print(v[1])
                                server_matrix[index][3] = str(v[1])
                            else:
                                # print(v[0])
                                server_matrix[index][3] = str(v[0])
                            count_done += 1
                index += 1
        count_done = 0
        for x in server_matrix:
            # print(x)
            if len(x[3]) < 1:
                received_ips = False
            else:
                count_done += 1
    print("")
    print("['                uuid                ', ' name '," +
          " 'root password', 'IP address']")
    for x in server_matrix:
        print(x)
else:
    print("Exiting...")
    sys.exit(1)
