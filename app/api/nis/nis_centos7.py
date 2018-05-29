#!/usr/bin/python
# -*- coding: utf-8 -*-

from common import utils, exception
from common.ansible_task import AnsibleTask


class Nis():
    def _check_params(self, require_params):
        for params in require_params:
            if not self.__dict__[params]:
                raise exception.ParamsMissing(params)

    def _get_extra_var(self, need_variable_names):
        extra_var = {}
        for params in need_variable_names:
            extra_var[params] = self.__dict__[params]
        return extra_var


class NisServer(Nis):
    """
    安装部署nis服务端
    参数:
        domain_name: 共享目录
        nis_server_host: nis服务端IP或主机名
    """

    def __init__(self, **kwargs):
        self.args = utils.convert(kwargs)
        self.domain_name = self.args.get('domain_name', None)
        self.nis_server_host = self.args.get('nis_server_host', {})

        self.need_variable_names = ["domain_name", "nis_server_host"]
        self.require_params = ["domain_name", "nis_server_host"]
        self._check_params(self.require_params)

        self._state = self.args.get("state", "install")
        self.task_name = "nis_server_%s" % self._state
        self.target_hosts = [self.nis_server_host]
        self.extra_var = self._get_extra_var(self.need_variable_names)

    def run(self):
        return AnsibleTask(self.task_name, self.extra_var).api_run(self.target_hosts)


class NisClient(Nis):
    """
    安装部署nis客户端
    参数:
        domain_name: 共享目录
        nis_server_host: nis服务端IP或主机名
        nis_client_hosts: 客户端主机信息
        格式:'nis_client_hosts': [
            "192.168.0.7": {
                "float_ip": '10.61.104.20',
                "hostname": 'nis-sge-client',
                "username": 'root',
                "password": 'root'
                },
            ]
    """

    def __init__(self, **kwargs):
        self.args = utils.convert(kwargs)
        self.domain_name = self.args.get('domain_name', None)
        self.nis_server_host = self.args.get('nis_server_host', {})
        self.nis_client_hosts = self.args.get('nis_client_hosts', [])

        self.need_variable_names = ["domain_name", "nis_server_host"]
        self.require_params = ["domain_name", "nis_server_host", "nis_client_hosts"]
        self._check_params(self.require_params)

        self._state = self.args.get("state", "install")
        self.task_name = "nis_client_%s" % self._state
        self.target_hosts = self.nis_client_hosts
        self.extra_var = self._get_extra_var(self.need_variable_names)
        self.extra_var["nis_server_host"] = self.nis_server_host["ip"]

    def run(self):
        return AnsibleTask(self.task_name, self.extra_var).api_run(self.target_hosts)
