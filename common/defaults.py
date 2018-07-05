import os

# ANSIBLE_CONFIG_PATH = "/etc/ansible"
# ANSIBLE_CONFIG_PATH = "/Users/huozhihui/zhi/ansible_project/ansible_sge_deploy"
# ANSIBLE_HOSTS_FILE = os.path.join(ANSIBLE_CONFIG_PATH, "hosts")
# ANSIBLE_SIT1_FILE = os.path.join(ANSIBLE_CONFIG_PATH, "sit1.yml")
# ANSIBLE_SIT2_FILE = os.path.join(ANSIBLE_CONFIG_PATH, "sit2.yml")

# log
LOG_PATH = "sge.log"
LOG_FORMAT = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(message)s"

# ansible
ANSIBLE_CONFIG_PATH = "/usr/local/ansible_deploy"

# sge cluster
CLUSTER_INFO_PATH = "/var/log/sge/cluster_info"
CLUSTER_NODES_NUMBER_PATH = "/var/log/sge/"
SGE_MASTER_HOSTNAME = "sge-master"
SGE_COMPUTE_HOSTNAME = "sge-compute"
