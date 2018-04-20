#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:5000/api/v1.0/nis_client"
params = {
    'state': 'install',
    'os': 'centos7',
    'domain_name': 'rzl',
    'nis_server_host': {
        "192.168.0.16": {
            "float_ip": '10.61.104.20',
            "hostname": 'test-sge-server',
            "username": 'root',
            "password": 'root'
        },
    },
    'nis_client_hosts': {
        "192.168.0.10": {
            "float_ip": '10.61.104.21',
            "hostname": 'test-sge-client-1',
            "username": 'root',
            "password": 'root'
        },
    }
}
header = {'Content-Type': 'application/json'}

data_str = json.dumps(params)
r = requests.post(url, data=data_str, headers=header)

print r.url
print r.text
print r.status_code
