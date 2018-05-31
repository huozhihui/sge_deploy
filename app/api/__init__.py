#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
from flask import Blueprint
from flask_restful import Api, Resource
from common.defaults import CLUSTER_INFO_PATH

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from app.api.sge_api import SgeClientApi, SgeMasterApi, SgeAuthApi
from app.api.nfs_api import NfsClientApi, NfsServerApi
from app.api.nis_api import NisServerApi, NisClientApi
from app.api.repo_api import RepoApi


class GetTaskApi(Resource):
    def get(self, id):
        path = os.path.join(CLUSTER_INFO_PATH, str(id))
        if not os.path.exists(path):
            return {"taskStatus": "running", "results": []}
        else:
            with open(path, 'r') as f:
                result = json.loads(f.read())
            return {"taskStatus": "completed", "results": result}


# 设置路由
api.add_resource(GetTaskApi, "/task/<int:id>")
api.add_resource(SgeMasterApi, "/sge/master")
api.add_resource(SgeClientApi, "/sge/client")
api.add_resource(SgeAuthApi, "/sge/auth")

api.add_resource(NfsServerApi, "/nfs/server")
api.add_resource(NfsClientApi, "/nfs/client")

api.add_resource(NisServerApi, "/nis/server")
api.add_resource(NisClientApi, "/nis/client")

api.add_resource(RepoApi, "/repo")
