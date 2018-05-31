#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import traceback
import urllib2
import threading
import json
from datetime import datetime
from retry import retry
from common.defaults import CLUSTER_INFO_PATH


def execute_success(task_id):
    return {"result": "true", "taskId": task_id}


def execute_fail(task_id, e):
    traceback.print_exc()
    err = "%s: %s" % (e.__class__.__name__, e.message)
    return {"result": "false", "error": err, "taskId": task_id}, 500


# 获取任务ID
def generate_task_id():
    return datetime.now().strftime("%Y%m%d%H%M%S")


# 获取任务存放路径
def get_task_path(task_id):
    if not os.path.exists(CLUSTER_INFO_PATH):
        os.makedirs(CLUSTER_INFO_PATH)
    return os.path.join(CLUSTER_INFO_PATH, task_id)


# 保存任务信息
def save_task_result(task_id, result):
    path = get_task_path(task_id)
    with open(path, 'w') as f:
        f.write(json.dumps(result, indent=4))

    if os.path.exists(path):
        return True
    else:
        return False


# 生成线程
def generate_thread(task_id, instance, log):
    t = threading.Thread(target=do_task, args=(task_id, instance, log,))
    t.start()


def do_task(task_id, instance, log):
    log.info("taskName: %s" % instance.task_name)
    log.info("taskHosts: %s" % instance.target_hosts)
    log.info("taskExtraVar: %s" % instance.extra_var)
    try:
        result = instance.run()
        log.info("taskResult: %s" % result)
        save_task_result(task_id, result)
    except Exception, e:
        return execute_fail(task_id, e)

# 通过线程执行任务, 任务完成后调用回调函数
# def do_task(instance, log, **kwargs):
#     requrl = kwargs.get("callbackUrl", None)
#     log.info("Task name: %s" % instance.task_name)
#     log.info("Target hosts: %s" % instance.target_hosts)
#     log.info("Task extra var: %s" % instance.extra_var)
#     try:
#         result = instance.run()
#         if requrl:
#             callback(requrl, result, log)
#         else:
#             log.info("Task result: %s" % result)
#     except Exception, e:
#         return execute_fail(e)


# 回调函数
# 回调失败后，重试3次，重试间隔时间1，5，10，20
# @retry(Exception, tries=4, delay=5, backoff=2)
# def callback(requrl, result, log):
#     # send_data = urllib.urlencode({"result": result})
#     send_data = json.dumps(result)
#     log.info("Begin request a callback......")
#     log.info("callback url: %s" % requrl)
#     log.info("send date: %s" % send_data)
#     req = urllib2.Request(url=requrl, data=send_data)
#     req.add_header('Content-Type', 'application/json')
#     req.get_method = lambda: 'PUT'
#     urllib2.urlopen(req).read()
#     log.info("Request a callback successfully!")
