#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:5000/api/v1/sge/addexec"
# url = "http://10.61.104.15:80/api/v1/sge/master"
url = "http://10.42.12.160:80/api/v1/sge/addexec"
params = {
    "os": "centos7",
    "state": "install",
    "sge_install_dir": "/opt",
    "sge_root_name": "sge",
    "sge_cluster_name": "rzl",
    "repo": "http://mirrors.ronglian.com/repo/Centos-7.repo",
    "queue_name": "abc",
    "sge_master_host": {
        "ip": "192.168.1.9",
        "hostname": "sge-master",
        "username": "root",
        "password": "root",
    },
    'sge_execd_hosts': [
        # {
        #     "ip": "192.168.1.13",
        #     "hostname": "sge-client-1",
        #     "username": "root",
        #     "password": "root",
        # },
        {
            "ip": "192.168.1.12",
            "hostname": "sge-client-2",
            "username": "root",
            "password": "root",
        },
    ],
}

header = {'Content-Type': 'application/json'}

data_str = json.dumps(params)
r = requests.post(url, data=data_str, headers=header)

print r.url
print r.text
print r.status_code
