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
Challenge 8:
Write a script that will create a static webpage served out of Cloud Files.
The script must create a new container, cdn enable it, enable it to serve
an index file, create an index file object, upload the object to the container,
and create a CNAME record pointing to the CDN URL of the container.
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

print("Please enter the name of the CDN container you wish to create:"),
cdn_cont = raw_input()
cdn_cont = cdn_cont.strip()

cf = pyrax.cloudfiles
cont = cf.list_containers()

dst_exists = False
for c in cont:
    if c == cdn_cont:
        dst_exists = True
        print("Containter '" + c + "' already exists. Proceed anyway? y/n: ")
        ans = raw_input()
        if ans != "y":
            sys.exit(1)

if not dst_exists:
    #create container
    dst = cf.create_container(cdn_cont)
    print("Created conainer '" + dst.name + "'.")
    print("Enabling container for CDN...")
    pyrax.cloudfiles.make_container_public(dst.name, ttl=900)
    # Set meta data for the container
    meta_data = {"X-Container-Meta-Web-Index": "index.html"}
    cf.set_container_metadata(dst, meta_data)
    print("Done.")
