#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
安装部署sge master
参数:
    sge_install_dir: sge安装目录
    sge_root_name: sge根名称
    sge_cluster_name: 集群名称
    sge_execd_hosts: 执行主机列表
        格式:
        sge_execd_hosts = {
            "192.168.0.5": {
                "float_ip": '10.61.104.111',
                "hostname": 'nis-sge-server',
                "username": 'root',
                "password": 'root'
            },
        }
"""
from copy import deepcopy

from common import utils, exception
from common.ansible_task import AnsibleTask

REQUIRE_PARAMS = ["sge_master_host"]
DEFAULT_PARAMS = ["sge_install_dir", "sge_root_name", "sge_cluster_name", "sge_admin_user", "queue_name"]


class Sge():
    def __init__(self, **kwargs):
        self.args = utils.convert(kwargs)
        self.sge_install_dir = self.args.get('sge_install_dir', '/opt')
        self.sge_root_name = self.args.get('sge_root_name', 'sge')
        self.sge_cluster_name = self.args.get('sge_cluster_name', 'rzl')
        self.sge_admin_user = self.args.get('sge_admin_user', 'root')
        self.sge_master_host = self.args.get('sge_master_host', {})
        self.sge_execd_hosts = self.args.get('sge_execd_hosts', [])
        self.queue_name = self.args.get('queue_name', "")
        self._check_params()
        self.extra_var = self._generate_extra_var()

    def _check_params(self):
        for params in REQUIRE_PARAMS:
            if not self.__dict__[params]:
                raise exception.ParamsMissing(params)

    def _generate_extra_var(self):
        extra_var = {}
        for params in REQUIRE_PARAMS:
            extra_var[params] = self.__dict__[params]

        for params in DEFAULT_PARAMS:
            extra_var[params] = self.__dict__[params]
        return extra_var

    def _add_extra_var(self):
        # 判断sge_master_host和sge_execd_hosts字典参数中是否包含hostname键
        etc_hosts = []
        md = {}
        for key in ["ip", "hostname"]:
            if not self.sge_master_host.has_key(key):
                raise exception.ParamsMissing("sge_master_host<%s>" % key)
            md[key] = self.sge_master_host[key]
        etc_hosts.append(md)

        execd_hostname_list = []
        for d in self.sge_execd_hosts:
            ed = {}
            for key in ["ip", "hostname"]:
                if not d.has_key(key):
                    raise exception.ParamsMissing("sge_execd_host<%s>" % key)
                md[key] = self.sge_master_host[key]
            etc_hosts.append(ed)
            execd_hostname_list.append(d["hostname"])

        # 增加"etc_hosts"和"sge_execd_host_list"变量
        self.extra_var.update({
            "etc_hosts": etc_hosts,
            "sge_execd_host_list": ",".join(execd_hostname_list)
        })

    def _run_playbook(self, name, target_hosts, extra_var):
        task = AnsibleTask(name, extra_var)
        return task.api_run(target_hosts)
        # task.cmd_run(target_hosts)
        # task.run_and_retry(target_hosts)

    def master(self, way="install"):
        task_name = "sge_master_%s" % way
        target_hosts = [self.sge_master_host]
        self._add_extra_var()
        return self._run_playbook(task_name, target_hosts, self.extra_var)

    # 先在sge master增加计算节点,然后安装计算节点
    def master_add_exec(self):
        task_name = "sge_master_add_exec"
        target_hosts = self.sge_master_host
        self._add_extra_var()
        return self._run_playbook(task_name, target_hosts, self.extra_var)

    def client(self, way="install"):
        if not self.sge_execd_hosts:
            raise exception.ParamsMissing("sge_execd_hosts")

        task_name = "sge_client_%s" % way
        target_hosts = self.sge_execd_hosts
        self._add_extra_var()
        return self._run_playbook(task_name, target_hosts, self.extra_var)
