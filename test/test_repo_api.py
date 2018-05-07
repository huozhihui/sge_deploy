#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:5000/api/v1/repo"
params = {
    "repo": "http://mirrors.aliyun.com/repo/Centos-7.repo",
    'target_hosts': [
        {
            "float_ip": '10.42.12.156',
            "ip": "192.168.1.10",
            "hostname": 'nis-server',
            "username": 'root',
            "password": 'root'
        }
    ]
}
header = {'Content-Type': 'application/json'}

data_str = json.dumps(params)
r = requests.post(url, data=data_str, headers=header)

print r.url
print r.text
print r.status_code
