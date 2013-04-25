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
Challenge 12:
- Write an application that will create a route in mailgun so that when an 
  email is sent to <YourSSO>@apichallenges.mailgun.org it calls your 
  Challenge 1 script that builds 3 servers.
- Assumptions:
  Assume that challenge 1 can be kicked off by accessing 
  http://cldsrvr.com/challenge1 
- We have an internal mailgun account for this challenge. 
"""

import os
import sys
import string
import pyrax
import pyrax.exceptions as exc
import time

