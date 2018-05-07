#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:5000/api/v1/sge/master"
# url = "http://10.42.12.160:80/api/v1/sge/master"
# url = "http://10.61.104.15:80/api/v1/sge/master"
params = {
    "os": "centos7",
    "state": "install",
    'callback_url': "http://127.0.0.1:4000/sge/callback",
    "sge_install_dir": "/opt",
    "sge_root_name": "sge",
    "sge_admin_user": "root",
    "sge_cluster_name": "rzl",
    "sge_master_host": {
        "float_ip": "10.42.12.147",
        "ip": "192.168.1.9",
        "hostname": "sge-master",
        "username": "root",
        "password": "root",
    },
}

header = {'Content-Type': 'application/json'}

data_str = json.dumps(params)
r = requests.post(url, data=data_str, headers=header)

print "Request url: %s" % r.url
print "Status code: %s" % r.status_code
print "Respones: %s" % r.text
