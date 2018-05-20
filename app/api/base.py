#!/usr/bin/python
# -*- coding: utf-8 -*-
import traceback
import urllib
import urllib2
import threading


def execute_success():
    return {"result": "true"}


def execute_fail(e):
    traceback.print_exc()
    err = "%s: %s" % (e.__class__.__name__, e.message)
    return {"result": "false", "error": err}, 500


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
    # send_data = urllib.urlencode({"result": result})
    send_data = json.dumps(result)
    try:
        print "Callback url: %s" % requrl
        print "Send data: %s" % send_data
        req = urllib2.Request(url=requrl, data=send_data)
        req.add_header('Content-Type', 'application/json')
        req.get_method = lambda: 'PUT'
        urllib2.urlopen(req).read()
    except Exception, e:
        return execute_fail(e)
