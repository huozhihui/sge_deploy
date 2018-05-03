#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import Resource
import os
import argument
import base
from app.sge.sge_centos7 import Sge
from app.nfs.nfs_centos7 import Nfs


class SgeAuthApi(Resource):
    def get(self):
        return {"token": "true"}


class SgeMasterApi(Resource):
    def post(self):
        args = argument.sge_parser.parse_args(strict=True)
        try:
            sge = Sge(**args)
            result = sge.master(args.state)
            return {"result": result}
        except Exception, e:
            return base.execute_fail(e)


class SgeClientApi(Resource):
    def post(self):
        args = argument.sge_client_parser.parse_args(strict=True)
        try:
            sge = Sge(**args)
            sge.client(args.state)
            msg = "sge client %s success!" % args.state
            return base.execute_success(msg)
        except Exception, e:
            return base.execute_fail(e)


class AddSgeExecApi(Resource):
    def post(self):
        args = argument.sge_parser.parse_args(strict=True)
        try:
            sge = Sge(**args)
            result = sge.master_add_exec()
            if result[0].get('status') == "success":
                result = sge.client("install")
            return {"result": result}
        except Exception, e:
            return base.execute_fail(e)

            # class AddSgeExecApi(Resource):
            #     def post(self):
            #         args = argument.sge_cluster_parser.parse_args(strict=True)
            #         try:
            #             nfs_args = {"nfs_server_host": args["sge_master_hosts"],
            #                         "share_dir": os.path.join(args["sge_install_dir"], args["sge_root_name"]),
            #                         "share_ip_address": args["nfs_share_ip_address"],
            #                         "nfs_client_hosts": args["sge_execd_hosts"]
            #                         }
            #             nfs = Nfs(**nfs_args)
            #             sge = Sge(**args)
            #             if args.state == "install":
            #                 nfs.client()
            #                 sge.client()
            #                 msg = "Add sge compute nodes success!"
            #             elif args.state == "uninstall":
            #                 sge.client(args.state)
            #                 nfs.client(args.state)
            #                 msg = "Remove sge compute nodes success!"
            #             return base.execute_success(msg)
            #         except Exception, e:
            #             return base.execute_fail(e)


            # class SgeClusterApi(Resource):
            #     def post(self):
            #         args = argument.sge_cluster_parser.parse_args(strict=True)
            #
            #         nfs_args = {"nfs_server_host": args["sge_master_hosts"],
            #                     "share_dir": os.path.join(args["sge_install_dir"], args["sge_root_name"]),
            #                     "share_ip_address": args["nfs_share_ip_address"],
            #                     "nfs_client_hosts": args["sge_execd_hosts"]
            #                     }
            #         try:
            #             if args['state'] == "install":
            #                 msg = self.install(args, nfs_args)
            #             if args['state'] == "uninstall":
            #                 msg = self.uninstall(args, nfs_args)
            #             return base.execute_success(msg)
            #         except Exception, e:
            #             return base.execute_fail(e)
            #
            #     def install(self, args, nfs_args):
            #         sge = Sge(**args)
            #         sge.master()
            #
            #         nfs = Nfs(**nfs_args)
            #         nfs.server()
            #
            #         nfs.client()
            #         sge.client()
            #         return "sge cluster install success!"
            #
            #     def uninstall(self, args, nfs_args):
            #         sge = Sge(**args)
            #         sge.client("uninstall")
            #
            #         nfs = Nfs(**nfs_args)
            #         nfs.client("uninstall")
            #
            #         sge.master("uninstall")
            #         nfs.server("uninstall")
            #
            #         return "sge cluster uninstall success!"
