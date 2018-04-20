#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:5000/api/v1.0/sge/master"
params = {
    "os": "centos7",
    "state": "install",
    "sge_install_dir": "/opt",
    "sge_root_name": "sge",
    "sge_admin_user": "root",
    "sge_cluster_name": "rzl",
    "repo": "http://mirrors.ronglian.com/repo/Centos-7.repo",
    "sge_master_host": {
        "float_ip": "10.61.104.20",
        "ip": "192.168.0.5",
        "hostname": "test-sge-master",
        "username": "root",
        "password": "root",
    },
    "nfs_server_host": {
        "ip": "192.168.0.16",
        "hostname": "nfs-server",
        "username": "root",
        "password": "root",
    },
    "nis_server_host": {
        "ip": "192.168.0.17",
        "hostname": "nis-server",
        "username": "root",
        "password": "root",
    }
}

header = {'Content-Type': 'application/json'}

data_str = json.dumps(params)
r = requests.post(url, data=data_str, headers=header)

print r.url
print r.text
print r.status_code
