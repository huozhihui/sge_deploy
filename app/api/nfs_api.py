#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import reqparse, Resource

import base
import argument
from app.nfs.nfs_centos7 import NfsServer, NfsClient


class NfsServerApi(Resource):
    def post(self):
        args = argument.nfs_server_parser.parse_args(strict=True)
        try:
            result = NfsServer(**args).run()
            return {"result": result}
        except Exception, e:
            return base.execute_fail(e)


class NfsClientApi(Resource):
    def post(self):
        args = argument.nfs_client_parser.parse_args(strict=True)
        try:
            result = NfsClient(**args).run()
            return {"result": result}
        except Exception, e:
            return base.execute_fail(e)
