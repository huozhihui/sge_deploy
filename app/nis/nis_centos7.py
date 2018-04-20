#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
安装部署nis服务端及客户端
参数:
    domain_name: 共享目录
    nis_server_host: nis服务端IP或主机名
    nis_client_hosts: 客户端主机信息
        格式:'nis_client_hosts': {
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

REQUIRE_PARAMS = ["domain_name", "nis_server_host", "nis_client_hosts"]
DEFAULT_PARAMS = []


class Nis():
    def __init__(self, **kwargs):
        self.args = utils.convert(kwargs)
        self.domain_name = self.args.get('domain_name', None)
        self.nis_server_host = self.args.get('nis_server_host', {})
        self.nis_client_hosts = self.args.get('nis_client_hosts', {})
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

    def _run_playbook(self, name, target_hosts, extra_var):
        task = AnsibleTask(name, extra_var)
        task.cmd_run(target_hosts)

    def server(self, way="install"):
        task_name = "nis_server_%s" % way
        target_hosts = self.nis_server_host
        extra_var = self._config_extra_var()
        self._run_playbook(task_name, target_hosts, extra_var)

    def client(self, way="install"):
        task_name = "nis_client_%s" % way
        target_hosts = self.nis_client_hosts
        extra_var = self._config_extra_var()
        nis_server_ip_or_hostname = self.nis_server_host.keys()[0]
        extra_var.update({"nis_server_host": nis_server_ip_or_hostname})
        self._run_playbook(task_name, target_hosts, extra_var)
