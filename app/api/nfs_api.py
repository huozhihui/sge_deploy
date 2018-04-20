#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import reqparse, Resource

import base
import argument
from app.nfs.nfs_centos7 import Nfs


class NfsServerApi(Resource):
    def post(self):
        args = argument.nfs_parser.parse_args(strict=True)
        try:
            nfs = Nfs(**args)
            nfs.server(args.state)
            msg = "Nfs server %s success!" % args.state
            return base.execute_success(msg)
        except Exception, e:
            return base.execute_fail(e)


class NfsClientApi(Resource):
    def post(self):
        args = argument.nfs_client_parser.parse_args(strict=True)
        try:
            nfs = Nfs(**args)
            nfs.client(args.state)
            msg = "Nfs client %s success!" % args.state
            return base.execute_success(msg)
        except Exception, e:
            return base.execute_fail(e)
