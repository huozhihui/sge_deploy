#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import Resource
import argument
import base
from nfs.nfs_centos7 import NfsServer, NfsClient


class NfsServerApi(Resource):
    def post(self):
        args = argument.nfs_server_parser.parse_args(strict=True)
        instance = NfsServer(**args)
        base.generate_thread(instance, **args)


class NfsClientApi(Resource):
    def post(self):
        args = argument.nfs_client_parser.parse_args(strict=True)
        instance = NfsClient(**args)
        base.generate_thread(instance, **args)
