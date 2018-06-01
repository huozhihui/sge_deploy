#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import current_app
from flask_restful import Resource
import argument
import base
from nis.nis_centos7 import NisServer, NisClient


class NisServerApi(Resource):
    def post(self):
        args = argument.nis_server_parser.parse_args()
        task_id = base.generate_task_id()
        log = current_app.logger
        log.info("taskID: %s" % task_id)
        try:
            instance = NisServer(**args)
            base.generate_thread(task_id, instance, log)
            return base.execute_success(task_id)
        except Exception, e:
            log.error(e)
            return base.execute_fail(task_id, e)


class NisClientApi(Resource):
    def post(self):
        args = argument.nis_client_parser.parse_args()
        task_id = base.generate_task_id()
        log = current_app.logger
        log.info("taskID: %s" % task_id)
        try:
            instance = NisClient(**args)
            base.generate_thread(task_id, instance, log)
            return base.execute_success(task_id)
        except Exception, e:
            log.error(e)
            return base.execute_fail(task_id, e)
