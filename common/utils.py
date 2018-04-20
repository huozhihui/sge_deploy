#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import collections


class CmdExecuteError(Exception):
    def __init__(self, cmd):
        err = "Cmd execute: %s" % cmd
        Exception.__init__(self, err)


def execute_cmd(cmd, stdin=""):
    pipe = subprocess.PIPE
    proc = subprocess.Popen(cmd, shell=True, stdout=pipe,
                            stderr=pipe, stdin=pipe)
    out, err = proc.communicate(stdin)
    ret = proc.returncode
    if ret != 0:
        print err or out
        raise CmdExecuteError(cmd)
    return ret, out, err

def shell_no_exception(cmd, stdin=""):
    pipe = subprocess.PIPE
    proc = subprocess.Popen(cmd, shell=True, stdout=pipe,
                            stderr=pipe, stdin=pipe)
    out, err = proc.communicate(stdin)
    ret = proc.returncode
    return ret, out, err



# {u'name': u'zhi', u'age': u'18'} to {'name': 'zhi', 'age': '18'}
def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data
