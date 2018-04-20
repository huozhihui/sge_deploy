#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:5000/api/v1.0/sge/auth"
header = {}

r = requests.get(url, headers=header)

print r.url
print r.text
print r.status_code
