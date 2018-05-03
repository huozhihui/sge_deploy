#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api, Resource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from app.api.sge_api import SgeClientApi, SgeMasterApi, AddSgeExecApi, SgeAuthApi
from app.api.nfs_api import NfsClientApi, NfsServerApi
from app.api.nis_api import NisServerApi, NisClientApi

# 设置路由
api.add_resource(SgeMasterApi, "/sge/master")
api.add_resource(SgeClientApi, "/sge/client")
api.add_resource(AddSgeExecApi, "/sge/addexec")
api.add_resource(SgeAuthApi, "/sge/auth")

api.add_resource(NfsServerApi, "/nfs/server")
api.add_resource(NfsClientApi, "/nfs/client")

api.add_resource(NisServerApi, "/nis/server")
api.add_resource(NisClientApi, "/nis/client")
