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
Write a script that will create 2 Cloud Servers and add them as nodes to a new Cloud Load Balancer.
"""

import os
import sys
import string
import pyrax
import pyrax.exceptions as exc

print "Using credentials file: ~/.rackspace_cloud_credentials"
cred_file = os.path.expanduser("~/.rackspace_cloud_credentials")
try:
    pyrax.set_credential_file(cred_file)
except exc.AuthenticationFailed:
        print "Did you remember to replace the credential file with your actual username and api_key?"

if pyrax.identity.authenticated:
        print "Successfully authenticated."
else:
        print "Authentication failed. Exiting..."
        sys.exit(1)

cs = pyrax.cloudservers
print "You're about to create 2 Cloud Servers and attach them behind a newly created Cloud Load Balancer."
img_matrix = []
img_num = 0
for img in cs.images.list():
	img_num += 1
	img_matrix.append([img_num, str(img.id), str(img.name), str(img.status), str(img.progress)])

for i in img_matrix:
	print i

print "From the list above please select the image you want to build the servers from."
print "Image number: "
server_img_num = raw_input()
server_img_num = server_img_num.strip()
try:
	server_img_num = int(server_img_num)
except ValueError:
	print "Please enter an integer from the list above. Exiting..."
	sys.exit(1)

for server in cs.servers.list():
	print
	print server.name
	for k, v in server.networks.iteritems():
		if k == "private":
			print str(v[0]) 




sys.exit(1)




print "Please enter the name of the new Cloud Load Balancer: "
clb_name = raw_input()
clb_name = clb_name.strip()


clb = pyrax.cloud_loadbalancers
print "Creating loadbalancer '" + clb_name + "'."
