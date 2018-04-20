#!/usr/bin/python
# -*- coding: utf-8 -*-
import traceback

def execute_success(msg):
    return {"success": "true", "msg": msg}

def execute_fail(e):
    traceback.print_exc()
    err = "%s: %s" % (e.__class__.__name__, e.message)
    return {"error": err}, 500