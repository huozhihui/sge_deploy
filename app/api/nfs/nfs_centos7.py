#!/usr/bin/python
# -*- coding: utf-8 -*-

from common import utils, exception
from common.ansible_task import AnsibleTask


class Nfs(object):
    def __init__(self, **kwargs):
        self.args = utils.convert(kwargs)
        self.nfs_server_host = self.args.get('nfsServerHost', {})
        self.share_dir = self.args.get('shareDir', None)

        self.need_variable_names = ["nfs_server_host", "share_dir"]
        self.require_params = ["nfs_server_host", "share_dir"]
        self._state = self.args.get("state", "install")

        self.task_name = "nfs"
        self.target_hosts = []
        self.extra_var = []

    def _check_params(self):
        for params in self.require_params:
            if not self.__dict__[params]:
                raise exception.ParamsMissing(params)

    def _get_extra_var(self):
        extra_var = {}
        for params in self.need_variable_names:
            extra_var[params] = self.__dict__[params]
        return extra_var

    def run(self):
        return AnsibleTask(self.task_name, self.extra_var).api_run(self.target_hosts)


class NfsServer(Nfs):
    """
    安装部署nfs服务端
    参数:
        share_dir: 共享目录
        share_ip_address: 共享ip范围, 格式: 192.168.0.0/24
        share_mode: 共享权限, 默认: rw,no_root_squash,no_all_squash,sync,anonuid=501,anongid=501
        ntp_server_host: ntp server端ip
    """

    def __init__(self, **kwargs):
        super(NfsServer, self).__init__(**kwargs)
        self.share_ip_address = self.args.get('shareIpAddress', None)
        self.share_mode = self.args.get('shareMode', "rw,no_root_squash,no_all_squash,sync,anonuid=501,anongid=501")
        self.need_variable_names.extend(["share_ip_address", "share_mode"])
        self.require_params.append("share_ip_address")
        self._check_params()

        self.task_name = "nfs_server_%s" % self._state
        self.target_hosts = [self.nfs_server_host]
        self.extra_var = self._get_extra_var()


class NfsClient(Nfs):
    """
    安装部署nfs客户端
    参数:
        nfs_server_host: nis服务端IP或主机名
        share_dir: 共享目录
        nfs_client_hosts: 客户端主机信息
        格式:'nfs_client_hosts': [
            "192.168.0.7": {
                "float_ip": '10.61.104.20',
                "hostname": 'nis-sge-client',
                "username": 'root',
                "password": 'root'
                },
            ]
    """

    def __init__(self, **kwargs):
        super(NfsClient, self).__init__(**kwargs)
        self.nfs_client_hosts = self.args.get('nfsClientHosts', {})
        self.require_params.append("nfs_client_hosts")
        self._check_params()

        self.task_name = "nfs_client_%s" % self._state
        self.target_hosts = self.nfs_client_hosts
        self.extra_var = self._get_extra_var()
        self.extra_var["nfs_server_host"] = self.nfs_server_host["ip"]
