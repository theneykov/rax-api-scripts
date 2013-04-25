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
- Create 2 servers, supplying a ssh key to be installed at /root/.ssh/authorized_keys.
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

print("You are about to create three 512MB Ubuntu 12.04 LTS Cloud Servers.")
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

print("SSH key: " + ssh_key)
