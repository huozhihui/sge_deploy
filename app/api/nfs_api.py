#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import current_app
from flask_restful import Resource
import argument
import base
from nfs.nfs_centos7 import NfsServer, NfsClient


class NfsServerApi(Resource):
    def post(self):
        args = argument.nfs_server_parser.parse_args()
        task_id = base.generate_task_id()
        log = current_app.logger
        log.info("taskID: %s" % task_id)
        try:
            instance = NfsServer(**args)
            base.generate_thread(task_id, instance, log)
            return base.execute_success(task_id)
        except Exception, e:
            log.error(e)
            return base.execute_fail(task_id, e)


class NfsClientApi(Resource):
    def post(self):
        args = argument.nfs_client_parser.parse_args()
        task_id = base.generate_task_id()
        log = current_app.logger
        log.info("taskID: %s" % task_id)
        try:
            instance = NfsClient(**args)
            base.generate_thread(task_id, instance, log)
            return base.execute_success(task_id)
        except Exception, e:
            log.error(e)
            return base.execute_fail(task_id, e)
