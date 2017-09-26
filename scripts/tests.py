#!/usr/bin/env python
import docker
import logging
import os
import argparse
from kubernetes import client,config





# VERSON =os.getenv('DJANGO-V')
# REGISTRY=os.getenv('KS_DOCKER_REGISTRY')
#
#
# log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)
# logging.basicConfig(level = logging.DEBUG)
#
# def build(self, dockerfile='.'):
#     dockerfile="/app/go"
#     client = docker.DockerClient(base_url='tcp://192.168.30.129:5001')
#     log.info(client.images.build(path=dockerfile,tag="django:"+str(VERSON),forcerm=True))
# def push():
#     client = docker.DockerClient(base_url='tcp://192.168.30.129:5001')
#     client.api.tag
#     log.info(client.api.tag("django:"+str(VERSON), str(REGISTRY)+"/"+"django",str(VERSON)))
#     client.api
#
#     log.info(client.images.push(REGISTRY+"/"+"django:"+str(VERSON)))
#
# parser = argparse.ArgumentParser(description='args')
# subparser = parser.add_subparsers(dest='action')
# args = parser.parse_args()
# log.info(str(args))
# action = args.action
# action_build = subparser.add_parser("build", help="build image")
# action_push = subparser.add_parser("push", help="push image")
# if action == 'build':
#     build()
# elif action == 'push':
#     push()