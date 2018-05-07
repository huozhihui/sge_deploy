#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:5000/api/v1/nis/client"
params = {
    'state': 'install',
    'os': 'centos7',
    'callback_url': "http://127.0.0.1:4000/sge/callback",
    'domain_name': 'rzl',
    'nis_server_host': {
        "ip": "192.168.1.10"
    },
    'nis_client_hosts': [
        {
            "float_ip": '10.42.12.157',
            "ip": "192.168.1.13",
            "hostname": 'sge-client-1',
            "username": 'root',
            "password": 'root'
        },
    ]
}
header = {'Content-Type': 'application/json'}

data_str = json.dumps(params)
r = requests.post(url, data=data_str, headers=header)

print "Request url: %s" % r.url
print "Status code: %s" % r.status_code
print "Respones: %s" % r.text
