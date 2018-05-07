#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import reqparse


def _common_argument():
    parser = reqparse.RequestParser()
    parser.add_argument("state", choices=('install', 'uninstall'), required=True)
    parser.add_argument("os", type=str, default="centos7")
    parser.add_argument("callback_url", type=str)
    return parser


def _sge_master_argument():
    parser = _common_argument()
    parser.add_argument("sge_install_dir", type=str, default="/opt")
    parser.add_argument("sge_root_name", type=str, default="sge")
    parser.add_argument("sge_cluster_name", type=str, default="rzl")
    parser.add_argument("sge_admin_user", type=str, default="root")
    parser.add_argument("sge_master_host", type=dict, required=True)
    return parser


def _sge_client_argument():
    parser = _common_argument()
    parser.add_argument("sge_install_dir", type=str, default="/opt")
    parser.add_argument("sge_root_name", type=str, default="sge")
    parser.add_argument("sge_cluster_name", type=str, default="rzl")
    parser.add_argument("sge_master_host", type=dict, required=True)
    parser.add_argument("queue_name", type=str, default="")
    parser.add_argument("sge_execd_hosts", type=dict, action='append', required=True)
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
    parser = reqparse.RequestParser()
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
