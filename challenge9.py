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

parser = argparse.ArgumentParser(description='Create server and create DNS ' +
                                 'record to point to its IP address.')
parser.add_argument('--fqdn', '-n', required=True, help='FQDN')
parser.add_argument('--image', '-i', required=True, help='Image ID')
parser.add_argument('--flavor', '-f', required=True, help='Flavor ID')
args = parser.parse_args()

print("--fqdn: " + str(args.fqdn))
print("--image: " + str(args.image))
print("--flavor: " + str(args.flavor))
