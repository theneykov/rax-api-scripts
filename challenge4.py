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
Challenge 4:
Write a script that uses Cloud DNS to create a new A record when passed
a FQDN and IP address as arguments.
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

print("Please enter the IP address for the A record you wish to create:"),
rec_ip = raw_input()
rec_ip = rec_ip.strip()

print("Please enter the name of the A record to be created for '" +
      rec_ip + "'.")
print("e.g. (ftp.example.com):"),
rec_name = raw_input()
rec_name = rec_name.strip()
rec_dom = rec_name[rec_name.find(".")+1:]

dns = pyrax.cloud_dns
# see if domain exists
domain_exists = False
for domain in dns.get_domain_iterator():
    if str(domain.name) == rec_dom:
        print("Domain exists: " + str(domain.name))
        dom = domain
        domain_exists = True
        break

if not domain_exists:
    print("Domain doesn't exist. Creating domain '" + rec_dom + "'.")
    print("Please enter your email address:"),
    dom_email = raw_input()
    dom_email = dom_email.strip()
    dom = dns.create(name=rec_dom, emailAddress=dom_email)

dom_rec = [{
           "type": "A",
           "name": rec_name,
           "data": rec_ip
           }]

for rec in dom.list_records():
    # see if a record already exists
    if rec.name == rec_name:
        print("A record '" + rec_name + "' already exists. Exiting...")
        sys.exit(1)

# create the record
print("Creating 'A' record '" + rec_name + "' for IP '" + rec_ip + "'.")
dom.add_record(dom_rec)
print("Done.")
