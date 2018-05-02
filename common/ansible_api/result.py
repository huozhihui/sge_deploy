#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.plugins.callback import CallbackBase


class ResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        """
            self.host_result = {
            "192.168.1.1": {"status": "success", "task_name": ""},
            "192.168.1.2": {"status": "failed", "task_name": "", "error": ""},
            }
        """
        self.host_result = {}
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result
        self.host_result[result._host.get_name()] = {
            "status": "unreachable",
            "task_name": unicode(result._task.name),
            "error": result._result['msg']
        }

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result
        self.host_result[result._host.get_name()] = {
            "status": "success",
            "task_name": unicode(result._task.name),
        }

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result
        self.host_result[result._host.get_name()] = {
            "status": "failed",
            "task_name": unicode(result._task.name),
            "error": result._result['msg']
        }

# results_callback = ResultsCollector()
