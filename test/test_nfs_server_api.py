#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:5000/api/v1/nfs/server"
params = {
    'state': 'install',
    'os': 'centos7',
    'share_dir': '/opt/aaa',
    'share_ip_address': '192.168.1.0/24',
    'share_mode': 'rw,no_root_squash,no_all_squash,sync,anonuid=501,anongid=501',
    'nfs_server_host': {
        "float_ip": '10.42.12.156',
        "ip": "192.168.1.10",
        "hostname": 'nis-server',
        "username": 'root',
        "password": 'root'
    },
}
header = {'Content-Type': 'application/json'}

data_str = json.dumps(params)
r = requests.post(url, data=data_str, headers=header)

print r.url
print r.text
print r.status_code
