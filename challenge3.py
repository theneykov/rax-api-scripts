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
Challenge 3 
Write a script that accepts a directory as an argument as well as a container name. The script should upload the contents of the specified directory to the container (or create it if it doesn't exist). The script should handle errors appropriately. (Check for invalid paths, etc.)
"""

import os
import sys
import string
import pyrax
import pyrax.exceptions as exc
import time

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

print "Please enter the directory you wish to upload to Cloud Files: "
dir = raw_input()
dir = dir.strip()

# Check to see if it's a valid dir
if not os.path.exists(dir):
	print dir + ": No such file or directory. Exiting..."
	sys.exit(1)
else:
	if not os.path.isdir(dir):
		print dir + ": Path specified is not a directory. Exiting..."
		sys.exit(1)

print
print "Please enter the container name you want to upload to: "
dst_cont = raw_input()
dst_cont = dst_cont.strip()

cf = pyrax.cloudfiles
cont = cf.list_containers()

dst_exists = False
for c in cont:
	if c == dst_cont:
		dst_exists = True
		print "Containter '" + c + "' already exists."

if not dst_exists:
	#create container
	dst = cf.create_container(dst_cont)
	print "Created conainer '" + dst.name + "'."

upload_key, total_bytes = cf.upload_folder(dir, container=dst_cont)

print "Uploading: "
done = False
while not done:
	curr_bytes = pyrax.cloudfiles.get_uploaded(upload_key) 
	progress = float(curr_bytes)/float(total_bytes)*100
	time.sleep(1)
	sys.stdout.write("\r%d%%" %progress)    # or print >> sys.stdout, "\r%d%%" %i,
	sys.stdout.flush()
	if progress == 100:
		done = True
		print

print "Upload complete."
