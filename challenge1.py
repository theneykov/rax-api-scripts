#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

print "You are about to create three 512MB Ubuntu 12.04 LTS Cloud Servers."
print "Please enter the servers' base name (ie. type: web to create servers web1, web2, web3)"
print "Base name: ",
sys.stdout.write('')
cs_base_name = raw_input()

print "Server names will be: "
for i in range(1, 4):
	print cs_base_name + str(i) 

print "Proceed with creating server instances? y/n: ",
sys.stdout.write('')
answer = raw_input()

if answer == "y":
	#go
	cs = pyrax.cloudservers
	#grab the Ubuntu 12.04 LTS image
	for img in cs.images.list():
		if "Ubuntu 12.04 LTS" in img.name:
			cs_image = img
	#grab the 512NB flavor
	for flv in cs.flavors.list():
		if flv.ram == 512:
			cs_flavor = flv
	#create matrix to hold server information
	server_matrix = []
	
	for s in range(3):
		current_name = cs_base_name + str(s)
		print "Creating server: ", current_name
		#print "Image: ", cs_image.id
		#print "Flavor: ", cs_flavor.id
		#Create server:
		server = cs.servers.create(current_name, cs_image.id, cs_flavor.id)
		#Add server information to matrix
		server_matrix.append([str(server.id), str(server.name), str(server.adminPass), ""])
	print "Servers are building...waiting to obtain IP information."
	
	received_ips = False
	while not received_ips:		
		print "Not all IPs have been assigned. Sleeping for 30 seconds."
		time.sleep(30)
		print
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
	                	index += 1
		print "['                uuid                ', ' name ', 'root password', 'IP address']"
                for x in server_matrix:
                        print x
                        if len(x[3]) < 1:
                                received_ips = False
else:
	print "Aborting."
print
print "Done."
print 
