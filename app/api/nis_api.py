#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from flask_restful import Resource
import base
import argument
from app.nis.nis_centos7 import Nis


class NisServerApi(Resource):
    def post(self):
        args = argument.nis_parser.parse_args(strict=True)
        try:
            nis = Nis(**args)
            nis.server(args.state)
            msg = "nis server %s success!" % args.state
            return base.execute_success(msg)
        except Exception, e:
            return base.execute_fail(e)


class NisClientApi(Resource):
    def post(self):
        args = argument.nis_parser.parse_args(strict=True)
        try:
            nis = Nis(**args)
            nis.client(args.state)
            msg = "nis client %s success!" % args.state
            return base.execute_success(msg)
        except Exception, e:
            return base.execute_fail(e)
