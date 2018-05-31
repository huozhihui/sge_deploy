#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import current_app
from flask_restful import Resource
import argument
import base
from sge.sge_centos7 import SgeMaster, SgeClient


class SgeAuthApi(Resource):
    def get(self):
        return {"token": "true"}


class SgeMasterApi(Resource):
    def post(self):
        # args = argument.sge_master_parser.parse_args(strict=True)
        args = argument.sge_master_parser.parse_args()
        task_id = base.generate_task_id()
        log = current_app.logger
        log.info("taskID: %s" % task_id)
        try:
            instance = SgeMaster(**args)
            base.generate_thread(task_id, instance, log)
            return base.execute_success(task_id)
        except Exception, e:
            log.error(e)
            return base.execute_fail(task_id, e)


class SgeClientApi(Resource):
    def post(self):
        args = argument.sge_client_parser.parse_args()
        task_id = base.generate_task_id()
        log = current_app.logger
        log.info("taskID: %s" % task_id)
        try:
            instance = SgeClient(**args)
            base.generate_thread(task_id, instance, log)
            return base.execute_success(task_id)
        except Exception, e:
            log.error(e)
            return base.execute_fail(task_id, e)
