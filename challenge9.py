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
Challenge 9:
Write an application that when passed the arguments FQDN, image, and flavor 
it creates a server of the specified image and flavor with the same name as
the fqdn, and creates a DNS entry for the fqdn pointing to the server's 
public IP
"""

import argparse
import os
import sys
import string
import pyrax
import pyrax.exceptions as exc
import time


parser = argparse.ArgumentParser(description='Create server and create DNS ' +
                                 'record to point to its IP address.')
parser.add_argument('--fqdn', '-n', required=True, help='FQDN')
parser.add_argument('--image', '-i', required=True, help='Image ID')
parser.add_argument('--flavor', '-f', required=True, help='Flavor ID')
args = parser.parse_args()

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

print("")
print("Creating server with the following parameters:")
print("--fqdn: " + str(args.fqdn))
print("--image: " + str(args.image))
print("--flavor: " + str(args.flavor))

# create matrix to hold server information
server_matrix = []

cs = pyrax.cloudservers
# Create server:
server = cs.servers.create(str(args.fqdn), str(args.image), str(args.flavor))
# Add server information to matrix
server_matrix.append([str(server.id), str(server.name),
                     str(server.adminPass), ""])

received_ips = False
count_done = 0
while not received_ips:
    print("IPs have not been assigned yet. Sleeping for 30 seconds.")
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

fqdn = str(args.fqdn) 
fqdn_domain = fqdn[fqdn.find(".")+1:]

dns = pyrax.cloud_dns
# see if domain exists
domain_exists = False
for domain in dns.get_domain_iterator():
    if str(domain.name) == fqdn_domain:
        print("Domain exists: " + str(domain.name))
        dom = domain
        domain_exists = True
        break

if not domain_exists:
    # print("Domain doesn't exist. Creating domain '" + fqdn_domain + "'.")
    # print("Please enter your email address:"),
    # dom_email = raw_input()
    # dom_email = dom_email.strip()
    dom_email = "racker@rackspace.com"
    dom = dns.create(name=fqdn_domain, emailAddress=dom_email)

fqdn_rec = [{
             "type": "A",
             "name": fqdn,
             "data": str(server_matrix[0][3]),
             "ttl": 3600
             }]

for rec in dom.list_records():
    # see if a record already exists
    if rec.name == fqdn:
        print("A record '" + fqdn + "' already exists. Exiting...")
        sys.exit(1)

# create the record
print("Creating 'A' record '" + fqdn + "' for '" + str(server_matrix[0][3]) + "'.")
dom.add_record(fqdn_rec)
print("Done.")
