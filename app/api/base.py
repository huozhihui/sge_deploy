#!/usr/bin/python
# -*- coding: utf-8 -*-
import traceback
import urllib
import urllib2
import threading


def execute_success(msg):
    return {"success": "true", "msg": msg}


def execute_fail(e):
    traceback.print_exc()
    err = "%s: %s" % (e.__class__.__name__, e.message)
    return {"error": err}, 500


# 生成线程
def generate_thread(instance, **kwargs):
    t = threading.Thread(target=do_task, args=(instance,), kwargs=kwargs)
    t.start()


# 通过线程执行任务, 任务完成后调用回调函数
def do_task(instance, **kwargs):
    requrl = kwargs.get("callback_url", None)
    try:
        result = instance.run()
        if requrl:
            callback(requrl, result)
        else:
            print result
    except Exception, e:
        return execute_fail(e)


# 回调函数
def callback(requrl, result):
    send_data = urllib.urlencode({"result": result})
    try:
        req = urllib2.Request(url=requrl, data=send_data)
        urllib2.urlopen(req).read()
    except Exception, e:
        return execute_fail(e)
