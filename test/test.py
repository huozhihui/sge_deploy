#!/usr/bin/python
# -*- coding: utf-8 -*-
params = {
    'state': 'install',
    'os': 'centos7',
    'sge_install_dir': '/opt',
    'sge_root_name': 'sge',
    'sge_cluster_name': 'rzl',
    'sge_admin_user': 'root',
    'sge_master_hosts': {
        "ip": "192.168.0.5",
        "hostname": 'sge-master',
        "username": 'root',
        "password": 'root',
    },
    'nis_server_host': {
        "ip": "192.168.0.16",
        "hostname": 'nis-server',
        "username": 'root',
        "password": 'root'
    },
    'nfs_server_host': {
        "ip": "192.168.0.16",
        "hostname": 'nfs-server',
        "username": 'root',
        "password": 'root'
    },
    'repo': "http://mirrors.ronglian.com/repo/Centos-7.repo"
}

import json

with open("sge_master_params.json", 'w') as f:
    f.write(json.dumps(params, indent=4))
