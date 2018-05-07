#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import Resource
import base
import argument
from app.repo.repo import Repo


class RepoApi(Resource):
    def post(self):
        args = argument.repo_parser.parse_args(strict=True)
        instance = Repo(**args)
        base.generate_thread(instance, **args)
