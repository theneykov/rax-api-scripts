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
Challenge 7:
Write a script that will create 2 Cloud Servers and add them as nodes to a 
new Cloud Load Balancer.
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
    print("Did you remember to replace the credential file with your " +
          "actual username and api_key?")

if pyrax.identity.authenticated:
    print("Successfully authenticated.")
else:
    print("Authentication failed. Exiting...")
    sys.exit(1)

cs = pyrax.cloudservers
# Number of servers to create and attach behind a new Cloud Load Balancer
srv_count = 2

print("You're about to create " + str(srv_count) + " Cloud Servers and attach them " +
      "behind a newly created Cloud Load Balancer.")
print("")
print("List of available images:")
img_matrix = []
img_num = 0
for img in cs.images.list():
    if img.status == "ACTIVE":
        img_num += 1
        img_matrix.append([img_num, str(img.id), str(img.name)])

for i in img_matrix:
    print i

print("")
print("From the list above please select the image you want to build the " +
      "servers from.")
print("Image number:"),
server_img_num = raw_input()
server_img_num = server_img_num.strip()

try:
    server_img_num = int(server_img_num)
except ValueError:
    print("Please enter an integer from the list above. Exiting...")
    sys.exit(1)

for img in img_matrix:
    if img[0] == server_img_num:
        server_img_uuid = str(img[1])
        #print("You've selected: " + str(server_img_uuid))

flv_matrix = []
for flv in cs.flavors.list():
    # Matrix list number, flavor ID, name, ram, swap, VCPUs
    flv_matrix.append([str(flv.id), str(flv.name), str(flv.ram), str(flv.swap), str(flv.vcpus)])

print("")
print("List of available flavors:")
print("['#', '      Flavor Name      ', 'RAM', 'SWAP', 'vCPUs']")
for i in flv_matrix:
    print str(i)

print("")
print("From the list above please select the server flavor: ")
print("Flavor number:"),
server_flv_num = raw_input()
server_flv_num = server_flv_num.strip()

try:
	server_flv_num = int(server_flv_num)
except ValueError:
        print("Please enter an integer from the list above. Exiting...")
        sys.exit(1)

if server_flv_num >= 2 and server_flv_num <= 8:
    pass
else:
    print("Invalid flavor number. Exiting...")
    sys.exit(1)

print("")
print("Please enter the servers' base name (ie. type: web to create servers web1, webN etc...)")
print("Base name:"),
cs_base_name = raw_input()
cs_base_name = cs_base_name.strip()

print("Server names will be:")
for i in range(1, srv_count+1):
    print cs_base_name + str(i)

print("")
print("Please enter a name for the new load balancer:"),
lb_name = raw_input()
lb_name = lb_name.strip()

print("")
print("Proceed with creating server instances and load balancer? y/n:"),
answer = raw_input()

if answer == "y":
    #create matrix to hold server information
    server_matrix = []

    for s in range(1,srv_count+1):
        current_name = cs_base_name + str(s)
        print("Creating server: " + str(current_name))
        #print("Image: ", server_img_uuid)
        #print("Flavor: ", server_flv_num)
        #Create server:
        server = cs.servers.create(current_name, server_img_uuid, server_flv_num)
        #Add server information to matrix
        #                            uuid           name             root password,      publicnet,  servicenet
        server_matrix.append([str(server.id), str(server.name), str(server.adminPass), "", ""])
    print("Servers are building...waiting to obtain IP information.")

    received_ips = False
    while not received_ips:
        print("Server IPs have not been provisioned yet. Sleeping for 30 seconds.")
        time.sleep(30)
        received_ips = True
        #get server list and populate server_matrix with IPs
        for y in cs.servers.list():
            index = 0
            for s in server_matrix:
                if y.id == server_matrix[index][0]:
                    #print i.networks
                    for k, v in y.networks.iteritems():
                        if k == "public":
                            if len(v[0]) > 15:
                                #print v[1]
                                server_matrix[index][3] = str(v[1])
                            else:
                                #print v[0]
                                server_matrix[index][3] = str(v[0])
                        else:
                            server_matrix[index][4] = str(v[0])
                index += 1
        for check in server_matrix:
            if len(check[3]) < 1 or len(check[4]) < 1:
                received_ips = False
    print("['                uuid                ', ' name ', " +
          "'root password', '  Public IP  ', '  Service Net  ']")
    for x in server_matrix:
        print x

    print("")
    print("Creating Load Balancer " + lb_name + ".")
    clb = pyrax.cloud_loadbalancers
    lb_node = []
    index = 0
    for s in server_matrix:
        lb_node.append(clb.Node(address=str(server_matrix[index][4]), port=80, condition="ENABLED"))
        index += 1
    vip = clb.VirtualIP(type="PUBLIC")
    lb = clb.create(lb_name, port=80, protocol="HTTP", nodes=lb_node, virtual_ips=[vip])

    lb = clb.list()
    print("Current Cloud Load Balancers in this region:")
    for details in lb:
        print("")
        print("CLB: " + str(details.id) + " " + str(details.name) + " " + 
              str(details.status) + " " + str(details.virtual_ips) + " " +
              str(details.port) + " " + str(details.protocol))
        print("Nodes:")
        for n in details.nodes:
            print("      \- " + str(n.id) + " " + str(n.condition) + " " + 
                  str(n.status) + " " + str(n.type) + " " + 
                  str(n.address).strip() + ":" + str(n.port).strip())
else:
    sys.exit(0)
