#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
安装部署sge master
参数:
    sge_install_dir: sge安装目录
    sge_root_name: sge根名称
    sge_cluster_name: 集群名称, 默认rzl
    sge_admin_user: sge管理员用户, 默认root
    sge_execd_hosts: 执行主机列表
    举例: sge_execd_hosts = [
            {"hostip"="192.168.0.7", "hostname"="sge-client"},
            {"hostip"="192.168.0.8", "hostname"="sge-client2"}
          ]
"""
from copy import deepcopy

from common import utils, exception
from common.ansible_task import AnsibleTask

REQUIRE_PARAMS = ["sge_master_hosts", "sge_execd_hosts"]
DEFAULT_PARAMS = ["sge_install_dir", "sge_root_name", "sge_cluster_name", "sge_admin_user"]


class SgeMaster():
    def __init__(self, **kwargs):
        self.args = utils.convert(kwargs)
        self.sge_install_dir = self.args.get('sge_install_dir', '/opt')
        self.sge_root_name = self.args.get('sge_root_name', 'sge')
        self.sge_cluster_name = self.args.get('sge_cluster_name', 'rzl')
        self.sge_admin_user = self.args.get('sge_admin_user', 'root')
        self.sge_master_hosts = self.args.get('sge_master_hosts', {})
        self.sge_execd_hosts = self.args.get('sge_execd_hosts', {})
        self.target_hosts = self.sge_master_hosts
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

        master_hosts_list = []
        for key, value_dict in self.sge_master_hosts.items():
            if not value_dict.get("hostname", None):
                raise exception.ParamsMissing("sge_master_hosts<hostname>")
            master_hosts_list.append({"ip": key, "hostname": value_dict["hostname"]})
        extra_var.update({"sge_master_hosts": master_hosts_list})

        execd_hosts_list = []
        execd_hostname_list = []
        for key, value_dict in self.sge_execd_hosts.items():
            if not value_dict.get("hostname", None):
                raise exception.ParamsMissing("sge_execd_hosts<hostname>")
            execd_hostname_list.append(value_dict["hostname"])
            execd_hosts_list.append({"ip": key, "hostname": value_dict["hostname"]})

        # 修改sge_execd_hosts参数格式
        # 添加sge_execd_host_list参数
        extra_var.update({"sge_execd_hosts": execd_hosts_list,
                          "sge_execd_host_list": " ".join(execd_hostname_list)})
        return extra_var

    def install(self):
        task_name = "sge_master_install"
        extra_var = self._config_extra_var()
        task = AnsibleTask(task_name, self.target_hosts, extra_var)
        task.cmd_run()
        # task.api_run()

    def uninstall(self):
        task_name = "sge_master_uninstall"
        extra_var = self._config_extra_var()
        task = AnsibleTask(task_name, self.target_hosts, extra_var)
        task.cmd_run()