#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from result import ResultsCollector
from options import options


class AnsibleAPI(object):
    """
    This is a General object for parallel execute modules.
    """

    def __init__(self, resource, *args, **kwargs):
        self.resource = resource
        self.inventory = None
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = None
        self.__initializeData()
        self.results_raw = {}

    def __initializeData(self):
        """
        初始化ansible
        """
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources=self.resource)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.options = options
        self.passwords = dict(vault_pass='secret')
        # self.passwords = dict(sshpass=None, becomepass=None)

    def run(self, host_list, module_name, module_args):
        """
        run module from andible ad-hoc.
        module_name: ansible module_name
        module_args: ansible module args
        """
        # create play with tasks
        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args))]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        # actually run it
        tqm = None
        self.callback = ResultsCollector()
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
            )
            tqm._stdout_callback = self.callback
            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

    def run_playbook(self, extra_vars, playbooks):
        """
        run ansible palybook
        """
        try:
            self.callback = ResultsCollector()
            self.variable_manager.extra_vars = extra_vars
            executor = PlaybookExecutor(
                playbooks=playbooks, inventory=self.inventory, variable_manager=self.variable_manager,
                loader=self.loader, options=self.options, passwords=self.passwords,
            )
            executor._tqm._stdout_callback = self.callback
            executor.run()
        except Exception as e:
            print "error:", e.message

    def get_result(self):
        """

        Returns: [
            {"ip": "192.168.1.1", "status": "success", "task_name": ""},
            {"ip": "192.168.1.2", "status": "failed", "task_name": "", "error": ""},
        ]

        """
        res = []
        for host, info in self.callback.host_result.items():
            info["ip"] = host
            res.append(info)
        return res

    def get_result2(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = result._result['msg']

        for host, result in self.callback.host_failed.items():
            task_name = unicode(result._task.name)
            self.results_raw['failed'][host] = {"task_name": task_name,
                                                "error": result._result.get('msg') or result._result
                                                }

        for host, result in self.callback.host_ok.items():
            if not self.results_raw['failed'].has_key(host):
                self.results_raw['success'][host] = result._result.get('stdout') or result._result

        return self.results_raw


if __name__ == '__main__':
    resource = "/Users/huozhihui/zhi/ansible_project/ansible_deploy/hosts"
    playbooks = ["/Users/huozhihui/zhi/ansible_project/ansible_deploy/test.yml"]
    extra_var = {"sge_install_dir": "/opt1",
                 "sge_root_name": "sge1",
                 "sge_admin_user": "root",
                 "sge_master_host": "aa",
                 "sge_execd_hosts": "bb"
                 }
    extra_var = {"sge_root": "/opt/sge"}
    api = AnsibleAPI(resource)
    api.run_playbook(extra_var, playbooks)
    print api.get_result()
