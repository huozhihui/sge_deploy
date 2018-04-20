#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
安装部署nfs client
参数:
    share_dir: 共享目录
    share_ip: 共享ip范围, 格式: 192.168.0.0/24
    share_mode: 共享权限, 默认: rw,no_root_squash,no_all_squash,sync,anonuid=501,anongid=501
    ntp_server_host: ntp server端ip
    ntp_client_hosts: 客户端主机信息
        格式:'ntp_client_hosts': {
        "192.168.0.7": {
            "float_ip": '10.61.104.20',
            "hostname": 'nis-sge-client',
            "username": 'root',
            "password": 'root'
        },
        "192.168.0.10": {
            "float_ip": '10.61.104.18',
            "hostname": 'nis-sge-client',
            "username": 'root',
            "password": 'root'
        },
    }
"""
from common.ansible_task import AnsibleTask
from common import utils, exception

REQUIRE_PARAMS = ["nfs_server_host", "share_dir", "share_ip_address", "nfs_client_hosts"]
DEFAULT_PARAMS = ["share_mode"]


class NfsClient():
    def __init__(self, **kwargs):
        self.args = utils.convert(kwargs)
        self.nfs_server_host = self.args.get('nfs_server_host', None)
        self.share_dir = self.args.get('share_dir', None)
        self.share_ip_address = self.args.get('share_ip_address', None)
        self.share_mode = self.args.get('share_mode', "rw,no_root_squash,no_all_squash,sync,anonuid=501,anongid=501")
        self.nfs_client_hosts = self.args.get('nfs_client_hosts', {})
        self.target_hosts = self.nfs_client_hosts

        self._check_params()

    def _check_params(self):
        for params in REQUIRE_PARAMS:
            if not self.__dict__[params]:
                raise exception.ParamsMissing(params)

    def _config_extra_var(self):
        extra_var = {}
        for params in REQUIRE_PARAMS:
            extra_var[params] = self.__dict__[params]

        for params in DEFAULT_PARAMS:
            extra_var[params] = self.__dict__[params]

        return extra_var

    def install(self):
        task_name = "nfs_client_install"
        extra_var = self._config_extra_var()
        task = AnsibleTask(task_name, self.target_hosts, extra_var)
        task.cmd_run()

    def uninstall(self):
        task_name = "nfs_client_uninstall"
        extra_var = self._config_extra_var()
        task = AnsibleTask(task_name, self.target_hosts, extra_var)
        task.cmd_run()
