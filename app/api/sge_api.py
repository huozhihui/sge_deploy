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
        instance = SgeMaster(**args)
        log = current_app.logger
        base.generate_thread(instance, log, **args)
        return base.execute_success()


class SgeClientApi(Resource):
    def post(self):
        args = argument.sge_client_parser.parse_args()
        instance = SgeClient(**args)
        log = current_app.logger
        base.generate_thread(instance, log, **args)
        return base.execute_success()
