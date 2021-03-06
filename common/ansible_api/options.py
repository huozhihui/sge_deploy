from collections import namedtuple

Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks',
                                 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                                 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user',
                                 'verbosity', 'check', 'diff', 'timeout', 'log_path', 'host_key_checking'])

options = Options(listtags=False,
                  listtasks=False,
                  listhosts=False,
                  syntax=False,
                  connection='ssh',
                  module_path=None,
                  forks=100,
                  remote_user='root',
                  private_key_file=None,
                  ssh_common_args=None,
                  ssh_extra_args=None,
                  sftp_extra_args=None,
                  scp_extra_args=None,
                  become=False,
                  become_method=None,
                  become_user='root',
                  verbosity=None,
                  check=False,
                  diff=False,
                  timeout=60,
                  log_path="/var/log/ansible.log",
                  host_key_checking=False)
