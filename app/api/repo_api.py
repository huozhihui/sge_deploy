#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import Resource
import argument
import base
from repo.repo import Repo


class RepoApi(Resource):
    def post(self):
        args = argument.repo_parser.parse_args(strict=True)
        instance = Repo(**args)
        base.generate_thread(instance, **args)
