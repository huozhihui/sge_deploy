#!/usr/bin/python
# -*- coding: utf-8 -*-

from common import utils, exception
from common.ansible_task import AnsibleTask


class Base():
    def _check_params(self, require_params):
        for params in require_params:
            if not self.__dict__[params]:
                raise exception.ParamsMissing(params)

    def _get_extra_var(self, need_variable_names):
        extra_var = {}
        for params in need_variable_names:
            extra_var[params] = self.__dict__[params]
        return extra_var


class Repo(Base):
    """
    配置yum源
    参数:
        repo_url: yum源地址
        target_hosts: 目标主机
    """

    def __init__(self, **kwargs):
        self.args = utils.convert(kwargs)
        self.repo = self.args.get('repo', None)
        self.target_hosts = self.args.get('target_hosts', [])

        self.require_params = ["repo", "target_hosts"]
        self._check_params(self.require_params)

        self.task_name = "repo_config"
        self.need_variable_names = ["repo"]
        self.extra_var = self._get_extra_var(self.need_variable_names)

    def run(self):
        return AnsibleTask(self.task_name, self.extra_var).api_run(self.target_hosts)
