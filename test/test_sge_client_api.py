#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:5000/api/v1/sge/client"
# url = "http://10.42.12.160:80/api/v1/sge/client"
params = {
    "os": "centos7",
    "state": "install",
    'callbackUrl': "http://127.0.0.1:4000/sge/callback",
    "sgeInstallDir": "/opt",
    "sgeRootName": "sge",
    "sgeClusterName": "rzl",
    "queueName": "abc",
    "sgeMasterHost": {
        "floatIp": "10.42.12.147",
        "ip": "192.168.1.9",
        # "hostname": "sge-master",
        "username": "root",
        "password": "root",
    },
    'sgeExecdHosts': [
        {
            "floatIp": "10.42.12.157",
            "ip": "192.168.1.13",
            # "hostname": "sge-client-1",
            "username": "root",
            "password": "root",
        },
        {
            "floatIp": "10.42.12.150",
            "ip": "192.168.1.12",
            # "hostname": "sge-client-2",
            "username": "root",
            "password": "root",
        },
    ],
}
header = {'Content-Type': 'application/json'}

data_str = json.dumps(params)
r = requests.post(url, data=data_str, headers=header)

print "Request url: %s" % r.url
print "Status code: %s" % r.status_code
print "Respones: %s" % r.text
