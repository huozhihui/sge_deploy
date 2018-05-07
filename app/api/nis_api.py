#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from flask_restful import Resource
import base
import argument
from app.nis.nis_centos7 import NisServer, NisClient


class NisServerApi(Resource):
    def post(self):
        args = argument.nis_server_parser.parse_args(strict=True)
        try:
            result = NisServer(**args).run()
            return {"result": result}
        except Exception, e:
            return base.execute_fail(e)


class NisClientApi(Resource):
    def post(self):
        args = argument.nis_client_parser.parse_args(strict=True)
        try:
            result = NisClient(**args).run()
            return {"result": result}
        except Exception, e:
            return base.execute_fail(e)
