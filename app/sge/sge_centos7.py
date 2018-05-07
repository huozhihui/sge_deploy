#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.ansible_task import AnsibleTask
from common import utils, exception


class Sge():
    def _check_params(self, require_params):
        for params in require_params:
            if not self.__dict__[params]:
                raise exception.ParamsMissing(params)

        sge_master_host = self.__dict__["sge_master_host"]
        sge_exec_hosts = self.__dict__.get("sge_exec_hosts", [])

        for key in ["ip", "hostname"]:
            if not sge_master_host.has_key(key):
                raise exception.ParamsMissing("sge_master_host<%s>" % key)

        for d in sge_exec_hosts:
            for key in ["ip", "hostname"]:
                if not d.has_key(key):
                    raise exception.ParamsMissing("sge_execd_host<%s>" % key)

    def _get_extra_var(self, need_variable_names):
        extra_var = {}
        for params in need_variable_names:
            extra_var[params] = self.__dict__[params]

        return extra_var


class SgeMaster(Sge):
    """
    安装部署sge服务端
    参数:
        sge_install_dir: sge安装目录
        sge_root_name: sge根名称
        sge_cluster_name: 集群名称
        sge_admin_user: sge管理用户
        sge_master_host: sge master主机
    """

    def __init__(self, **kwargs):
        self.args = utils.convert(kwargs)
        self.sge_install_dir = self.args.get('sge_install_dir', '/opt')
        self.sge_root_name = self.args.get('sge_root_name', 'sge')
        self.sge_cluster_name = self.args.get('sge_cluster_name', 'rzl')
        self.sge_admin_user = self.args.get('sge_admin_user', 'root')
        self.sge_master_host = self.args.get('sge_master_host', {})

        self.need_variable_names = ["sge_install_dir", "sge_root_name", "sge_cluster_name", "sge_admin_user"]
        self.require_params = ["sge_master_host"]
        self._check_params(self.require_params)
        self._custom_check()

        self._state = self.args.get("state", "install")
        self.task_name = "sge_master_%s" % self._state
        self.target_hosts = [self.sge_master_host]
        self.extra_var = self._get_extra_var(self.need_variable_names)
        self._custom_extra_var()

    def _custom_check(self):
        for key in ["ip", "hostname"]:
            if not self.sge_master_host.has_key(key):
                raise exception.ParamsMissing("sge_master_host<%s>" % key)

    def _custom_extra_var(self):
        self.extra_var["etc_hosts"] = [
            {key: self.sge_master_host[key] for key in ["ip", "hostname"]}
        ]

    def run(self):
        return AnsibleTask(self.task_name, self.extra_var).api_run(self.target_hosts)


class SgeClient(Sge):
    """
    安装部署sge客户端
    参数:
        sge_install_dir: sge安装目录
        sge_root_name: sge根名称
        sge_cluster_name: 集群名称
        sge_master_host: sge master主机
        sge_execd_hosts: 执行主机列表
        queue_name: 队列名称
    """

    def __init__(self, **kwargs):
        self.args = utils.convert(kwargs)
        self.sge_install_dir = self.args.get('sge_install_dir', '/opt')
        self.sge_root_name = self.args.get('sge_root_name', 'sge')
        self.sge_cluster_name = self.args.get('sge_cluster_name', 'rzl')
        self.sge_master_host = self.args.get('sge_master_host', {})
        self.sge_execd_hosts = self.args.get('sge_execd_hosts', [])
        self.queue_name = self.args.get('queue_name', "")

        self.need_variable_names = ["sge_install_dir", "sge_root_name", "sge_cluster_name", "queue_name"]
        self.require_params = ["sge_master_host", "sge_execd_hosts"]
        self._check_params(self.require_params)
        self._custom_check()

        self._state = self.args.get("state", "install")
        self.task_name = "sge_client_%s" % self._state
        self.target_hosts = self.sge_execd_hosts
        self.extra_var = self._get_extra_var(self.need_variable_names)
        self._custom_extra_var()

    def _custom_check(self):
        for key in ["ip", "hostname"]:
            if not self.sge_master_host.has_key(key):
                raise exception.ParamsMissing("sge_master_host<%s>" % key)

        for d in self.sge_execd_hosts:
            for key in ["ip", "hostname"]:
                if not d.has_key(key):
                    raise exception.ParamsMissing("sge_execd_hosts<%s>" % key)

    def _custom_extra_var(self):
        etc_hosts = []
        execd_hostname_list = []

        etc_hosts.append({key: self.sge_master_host[key] for key in ["ip", "hostname"]})

        for d in self.sge_execd_hosts:
            etc_hosts.append({key: d[key] for key in ["ip", "hostname"]})
            execd_hostname_list.append(d["hostname"])

        # 增加"etc_hosts"和"sge_execd_host_list"变量
        self.extra_var.update({
            "etc_hosts": etc_hosts,
            "sge_execd_host_list": ",".join(execd_hostname_list)
        })

    def config_master(self):
        task_name = "sge_master_add_exec"
        target_hosts = [self.sge_master_host]
        return AnsibleTask(task_name, self.extra_var).api_run(target_hosts)

    def run(self):
        return AnsibleTask(self.task_name, self.extra_var).api_run(self.target_hosts)
