#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from common.ansible_task import AnsibleTask
from common import utils, exception
from common.defaults import CLUSTER_PATH, SGE_MASTER_HOSTNAME, SGE_COMPUTE_HOSTNAME


class Sge():
    def _check_params(self, require_params):
        for params in require_params:
            if not self.__dict__[params]:
                raise exception.ParamsMissing(params)

        sge_master_host = self.__dict__["sge_master_host"]
        sge_exec_hosts = self.__dict__.get("sge_exec_hosts", [])

        if not sge_master_host.has_key("ip"):
            raise exception.ParamsMissing("sge_master_host<ip>")

        for d in sge_exec_hosts:
            if not d.has_key("ip"):
                raise exception.ParamsMissing("sge_execd_host<ip>")

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
        self.sge_install_dir = self.args.get('sgeInstallDir', '/opt')
        self.sge_root_name = self.args.get('sgeRootName', 'sge')
        self.sge_cluster_name = self.args.get('sgeClusterName', 'rzl')
        self.sge_admin_user = self.args.get('sgeAdminUser', 'root')
        self.sge_master_host = self.args.get('sgeMasterHost', {})

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
        pass

    def _custom_extra_var(self):
        self.extra_var["etc_hosts"] = [{
            "ip": self.sge_master_host["ip"],
            "hostname": self.sge_master_host.get("hostname", SGE_MASTER_HOSTNAME)
        }]

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
        self.sge_install_dir = self.args.get('sgeInstallDir', '/opt')
        self.sge_root_name = self.args.get('sgeRootName', 'sge')
        self.sge_cluster_name = self.args.get('sgeClusterName', 'rzl')
        self.sge_master_host = self.args.get('sgeMasterHost', {})
        self.sge_execd_hosts = self.args.get('sgeExecdHosts', [])
        self.queue_name = self.args.get('queueName', "")

        self.need_variable_names = ["sge_install_dir", "sge_root_name", "sge_cluster_name", "queue_name"]
        self.require_params = ["sge_master_host", "sge_execd_hosts"]
        self._check_params(self.require_params)
        self._custom_check()

        self._state = self.args.get("state", "install")
        self.task_name = "sge_client_%s" % self._state
        self.target_hosts = self.sge_execd_hosts
        self.extra_var = self._get_extra_var(self.need_variable_names)
        self._custom_extra_var()

    # 获取集群计算节点个数并更新
    def _get_client_node_num(self):
        if not os.path.exists(CLUSTER_PATH):
            cluster_client_count = 0
        else:
            with open(CLUSTER_PATH, "r") as f:
                cluster_client_count = int(f.read())

        new_cluster_count = cluster_client_count + len(self.sge_execd_hosts)
        with open(CLUSTER_PATH, "w") as f:
            f.write(str(new_cluster_count))

        return cluster_client_count

    def _custom_check(self):
        pass

    def _custom_extra_var(self):
        etc_hosts = []
        execd_hostname_list = []

        etc_hosts.append({
            "ip": self.sge_master_host["ip"],
            "hostname": self.sge_master_host.get("hostname", SGE_MASTER_HOSTNAME)
        })

        cluster_client_count = self._get_client_node_num()
        for sge_execd_host in self.sge_execd_hosts:
            name = "%s%s" % (SGE_COMPUTE_HOSTNAME, cluster_client_count)
            hostname = sge_execd_host.get("hostname", name)
            etc_hosts.append({
                "ip": sge_execd_host["ip"],
                "hostname": hostname
            })
            execd_hostname_list.append(hostname)
            cluster_client_count += 1

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
        # 如果是安装,优先在sge master上做操作,如果操作失败直接返回错误
        if self._state == "install":
            result = self.config_master()
            if result[0].get('status') != "success":
                return result
        return AnsibleTask(self.task_name, self.extra_var).api_run(self.target_hosts)
