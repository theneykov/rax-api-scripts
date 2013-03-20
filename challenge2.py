#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ted Neykov
# 201303XX - Challenge 2
# Write a script that clones a server (takes an image and deploys the image as a new server).

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

print "Preparing to clone server..."
cs = pyrax.cloudservers

server_matrix = []
print "Servers in current region:"
srv_count = 0
for srv in cs.servers.list():
	srv_count += 1
	#print str(srv_count) + ") " + srv.id + " " + srv.name
	#add entry to matrix so user can select server number later to image
	server_matrix.append([srv_count,str(srv.id),str(srv.name)])	

if srv_count == 0:
	print "You don't have any NextGen servers in this region to create an image from."
	print "Can't continue. Exiting..."
	sys.exit(1)

#print "Server list:"
print
for s in server_matrix:
	print str(s[0]) + ") " + s[1] + " " + s[2] 

print
print "Please enter the number of the server you wish to clone: "
srv_num = raw_input()
try:
	srv_num = int(srv_num)
except:
	print "Value must be an integer. Exiting."
	sys.exit(1)
	
#srv_num = int(srv_num)
if srv_num > srv_count or srv_num <= 0:
	print "Error specifying server number: Outside of range. Exiting."
	sys.exit(1)

print "Please enter the name of the new image you wish to create: "
new_image_name = raw_input()

for c in server_matrix:
	if int(c[0]) == srv_num:
		print "Creating image '" + new_image_name + "' of server '" + c[2] + "' (" + c[1] + ") ."
		cs.servers.create_image(c[1], new_image_name)



#print "Server images in current region:"
#grab the Ubuntu 12.04 LTS image
#for img in cs.images.list("detailed=True"):
#	print img.id + " - " + img.name

#Create server from image img_id
#print "Creating server: ", current_name
#Create server:

srv_name = "delme2"
try:
	server = cs.servers.create(srv_name, "bad-image-name-test6f5e3600-9dd9-4ef6-9b14-4b5192370c44", "2")
except:
	print "Failed to build server from image."

