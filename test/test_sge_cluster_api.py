#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:5000/api/v1.0/sge_cluster"
params = {
    'state': 'uninstall',
    'os': 'centos7',
    'sge_install_dir': '/opt',
    'sge_root_name': 'sge',
    'sge_cluster_name': 'rzl',
    'sge_admin_user': 'root',
    'sge_master_hosts': {
        "192.168.0.16": {
            "float_ip": '10.61.104.20',
            "hostname": 'test-sge-server',
            "username": 'root',
            "password": 'root',
        },
    },
    'sge_execd_hosts': {
        "192.168.0.10": {
            "float_ip": '10.61.104.21',
            "hostname": "test-sge-client-1",
            "username": 'root',
            "password": 'root'
        },
        "192.168.0.15": {
            "float_ip": '10.61.104.15',
            "hostname": "test-sge-client-2",
            "username": 'root',
            "password": 'root'
        },
    },
    'nfs_share_ip_address': "192.168.0.0/24",
    'repo': "http://mirrors.ronglian.com/repo/Centos-7.repo"
}
header = {'Content-Type': 'application/json'}

data_str = json.dumps(params)
r = requests.post(url, data=data_str, headers=header)

print r.url
print r.text
print r.status_code
