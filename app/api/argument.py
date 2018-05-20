#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import reqparse


def _common_argument():
    parser = reqparse.RequestParser()
    parser.add_argument("state", choices=('install', 'uninstall'), required=True)
    parser.add_argument("os", type=str, default="centos7")
    parser.add_argument("callbackUrl", type=str)
    return parser


def _sge_master_argument():
    parser = _common_argument()
    parser.add_argument("sgeInstallDir", type=str, default="/opt")
    parser.add_argument("sgeRootName", type=str, default="sge")
    parser.add_argument("sgeClusterName", type=str, default="rzl")
    parser.add_argument("sgeAdminUser", type=str, default="root")
    parser.add_argument("sgeMasterHost", type=dict, required=True)
    return parser


def _sge_client_argument():
    parser = _common_argument()
    parser.add_argument("sgeInstallDir", type=str, default="/opt")
    parser.add_argument("sgeRootName", type=str, default="sge")
    parser.add_argument("sgeClusterName", type=str, default="rzl")
    parser.add_argument("sgeMasterHost", type=dict, required=True)
    parser.add_argument("queueName", type=str, default="")
    parser.add_argument("sgeExecdHosts", type=dict, action='append', required=True)
    return parser


def _nfs_server_argument():
    parser = _common_argument()
    parser.add_argument("share_dir", type=str, required=True)
    parser.add_argument("share_ip_address", type=str, required=True)
    parser.add_argument("share_mode", type=str,
                        default="rw,no_root_squash,no_all_squash,sync,anonuid=501,anongid=501")
    parser.add_argument("nfs_server_host", type=dict, required=True)
    return parser


def _nfs_client_argument():
    parser = _common_argument()
    parser.add_argument("share_dir", type=str, required=True)
    parser.add_argument("nfs_server_host", type=dict, required=True)
    parser.add_argument("nfs_client_hosts", type=dict, action='append', required=True)
    return parser


def _nis_server_argument():
    parser = _common_argument()
    parser.add_argument("domain_name", type=str, required=True)
    parser.add_argument("nis_server_host", type=dict, required=True)
    return parser


def _nis_client_argument():
    parser = _common_argument()
    parser.add_argument("domain_name", type=str, required=True)
    parser.add_argument("nis_server_host", type=dict, required=True)
    parser.add_argument("nis_client_hosts", type=dict, action='append', required=True)
    return parser


def _repo_argument():
    parser = _common_argument()
    parser.remove_argument("state")
    parser.remove_argument("os")
    parser.add_argument("repo", type=str, required=True)
    parser.add_argument("target_hosts", type=dict, action='append', required=True)
    return parser


sge_master_parser = _sge_master_argument()
sge_client_parser = _sge_client_argument()

nfs_server_parser = _nfs_server_argument()
nfs_client_parser = _nfs_client_argument()

nis_server_parser = _nis_server_argument()
nis_client_parser = _nis_client_argument()

repo_parser = _repo_argument()
