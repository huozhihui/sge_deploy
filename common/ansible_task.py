#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import random
import string
from ansible_api.ansible_api import AnsibleAPI
from defaults import ANSIBLE_CONFIG_PATH


class AnsibleError(Exception):
    pass


class HostsFileNotExist(Exception):
    def __init__(self, path):
        err = "ansible hosts file not found: %s" % path
        Exception.__init__(self, err)


class PlaybookExecuteError(Exception):
    def __init__(self, path):
        err = "playbook %s execute failure!" % path
        Exception.__init__(self, err)


class AnsibleTask():
    def __init__(self, task_name, extra_var):
        self.task_name = task_name
        self._extra_var = extra_var
        self._run_count = 1
        self._res = {}

        # 生成任务ID
        self.task_id = ''.join(random.sample(string.ascii_letters, 4))

        # ansible hosts文件路径
        self._host_path = "%s/%s_hosts" % (ANSIBLE_CONFIG_PATH, self.task_id)

        self._playbook_name = ["%s/%s.yml" % (ANSIBLE_CONFIG_PATH, task_name)]

    def _generate_hosts_file(self, target_hosts):
        if not target_hosts:
            raise AnsibleError("Target hosts not exists!")

        if not isinstance(target_hosts, list):
            raise AnsibleError("Target hosts not 'list'!")

        with open(self._host_path, 'w') as f:
            f.write("[%s]\n" % self.task_name)
            for d in target_hosts:
                host_ip = d.get("floatIp", None) or d.get("ip", None)
                username = d.get('username', None)
                password = d.get('password', None)
                port = d.get('port', 22)

                if not host_ip:
                    raise AnsibleError("Target host ip not exists!")
                else:
                    content_list = [host_ip]

                if username:
                    content_list.append("ansible_ssh_user=%s" % username)
                if password:
                    content_list.append("ansible_ssh_pass=%s" % password)
                content_list.append("ansible_ssh_port=%s" % port)
                os.system("ssh-keygen -R %s >/dev/null 2>&1" % host_ip)
                s = " ".join(content_list)
                f.write(s)
                f.write("\n")

        if not os.path.exists(self._host_path):
            raise HostsFileNotExist(self._host_path)

    @staticmethod
    def _clear_file(path):
        if os.path.exists(path):
            os.remove(path)

    def cmd_run(self, target_hosts):
        self._generate_hosts_file(target_hosts)
        cmd = 'ansible-playbook -i %s -e "%s" %s' % (self._host_path, self._extra_var, self._playbook_name[0])
        print cmd
        res = os.system(cmd)
        self._clear_file(self._host_path)
        if res != 0:
            raise PlaybookExecuteError(self._playbook_name[0])

    def api_run(self, target_hosts):
        self._generate_hosts_file(target_hosts)
        print "Hosts file: %s" % self._host_path
        print "Extra var: %s" % self._extra_var
        print "Playbooks: %s" % ",".join(self._playbook_name)
        api = AnsibleAPI(self._host_path)
        api.run_playbook(self._extra_var, self._playbook_name)
        self._clear_file(self._host_path)
        return api.get_result()


if __name__ == '__main__':
    task_name = "sge_master_install"
    target_hosts = [
        {
            "float_ip": '10.61.104.20',
            "hostname": 'sge-master',
            "username": 'root',
            "password": 'root'
        },
        # {
        #     "float_ip": '10.61.104.22',
        #     "hostname": 'sge-master',
        #     "username": 'root',
        #     "password": 'root'
        # }
    ]

    extra_var = {"sge_root": "sge"}

    task_name = "test"

    task = AnsibleTask(task_name, extra_var)
    res = task.run_and_retry(target_hosts)
    print res
