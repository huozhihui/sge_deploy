#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import reqparse


def _common_argument():
    parser = reqparse.RequestParser()
    parser.add_argument("state", choices=('install', 'uninstall'), required=True)
    parser.add_argument("os", type=str, default="centos7")
    return parser


def _sge_argument():
    parser = _common_argument()
    parser.add_argument("sge_install_dir", type=str, default="/opt")
    parser.add_argument("sge_root_name", type=str, default="sge")
    parser.add_argument("sge_cluster_name", type=str, default="rzl")
    parser.add_argument("sge_admin_user", type=str, default="root")
    parser.add_argument("sge_master_host", type=dict, required=True)
    parser.add_argument("queue_name", type=str)
    parser.add_argument("nis_server_host", type=dict)
    parser.add_argument("nfs_server_host", type=dict)
    parser.add_argument("repo", type=str)
    return parser


def _sge_client_argument():
    parser = _sge_argument()
    parser.add_argument("sge_execd_hosts", type=dict, required=True)
    parser.remove_argument("sge_admin_user")
    return parser


def _sge_cluster_argument():
    parser = _sge_argument()
    parser.add_argument("sge_execd_hosts", type=dict, required=True)
    parser.add_argument("nfs_share_ip_address", type=str, required=True)
    return parser


def _nfs_argument():
    parser = _common_argument()
    parser.add_argument("share_dir", type=str, required=True)
    parser.add_argument("share_ip_address", type=str, required=True)
    parser.add_argument("share_mode", type=str,
                        default="rw,no_root_squash,no_all_squash,sync,anonuid=501,anongid=501")
    parser.add_argument("nfs_server_host", type=dict, required=True)
    return parser


def _nfs_client_argument():
    parser = _nfs_argument()
    parser.add_argument("nfs_client_hosts", type=dict, required=True)
    return parser


def _nis_argument():
    parser = _common_argument()
    parser.add_argument("domain_name", type=str, required=True)
    parser.add_argument("nis_server_host", type=dict, required=True)
    parser.add_argument("nis_client_hosts", type=dict, required=True)
    return parser


sge_parser = _sge_argument()
sge_client_parser = _sge_client_argument()
sge_cluster_parser = _sge_cluster_argument()
nfs_parser = _nfs_argument()
nfs_client_parser = _nfs_client_argument()
nis_parser = _nis_argument()
