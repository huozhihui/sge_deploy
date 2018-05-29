#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import Resource
import argument
import base
from nis.nis_centos7 import NisServer, NisClient


class NisServerApi(Resource):
    def post(self):
        args = argument.nis_server_parser.parse_args(strict=True)
        instance = NisServer(**args)
        base.generate_thread(instance, **args)


class NisClientApi(Resource):
    def post(self):
        args = argument.nis_client_parser.parse_args(strict=True)
        instance = NisClient(**args)
        base.generate_thread(instance, **args)
