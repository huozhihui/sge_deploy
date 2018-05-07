#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import Resource
import base
import argument
from app.repo.repo import Repo


class RepoApi(Resource):
    def post(self):
        args = argument.repo_parser.parse_args(strict=True)
        try:
            repo = Repo(**args)
            result = repo.run()
            return {"result": result}
        except Exception, e:
            return base.execute_fail(e)
