#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:5000/api/v1.0/sge/auth"
header = {}

r = requests.get(url, headers=header)

print "Request url: %s" % r.url
print "Status code: %s" % r.status_code
print "Respones: %s" % r.text
