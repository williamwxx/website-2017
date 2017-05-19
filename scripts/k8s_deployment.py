#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2016-09-09 上午10:12
@author: chenyongbing
@file: container.py
'''
import os , re ,etcd , time , json , commands
import logging
from docker import Client

from kubernetes import K8sConfig , K8sDeployment , K8sContainer,K8sVolumeMount , K8sVolume,K8sService
current_dir = os.path.split(os.path.realpath(__file__))[0]
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


class K8sDeployment(K8sDeployment):
    def set_container_image(self, name=None, image=None):
        containers = []
        for c in self.model.spec.template.spec.containers:
            if c.name == name:
                c.image = image
            containers.append(c)
        self.model.spec.template.spec.containers = containers
        # self.model.spec.template.spec.image_pull_secrets=[{'name':'myregistrykey'}]
        return self

    def _exists(self):
        try:
            self.get()
            return True
        except:
            return False


    def add_change_cause(self,msg):
        self.model.metadata.annotations['kubernetes.io/change-cause'] = msg
    def add_volume(self,volume):
        volumes = self.model.spec.template.spec.volumes
        if volume not in volumes:
            volumes.append(volume.model)
        return self

    def change_container_resources_limits(self,**kwargs):
        for container in self.containers:
            container.model.resources.limits = kwargs

class K8sContainer(K8sContainer):
    def add_image_pull_policy(self,policy):
        self.model.image_pull_policy=policy

    def add_container_resources_requests(self,**kwargs):
        self.model.resources.requests = kwargs


    def add_container_resources_limits(self,**kwargs):
        self.model.resources.limits = kwargs

class K8sService(K8sService):
    def _exists(self):
        try:
            self.get()
            return True
        except:
            return False

    def del_port(self):
        for p in self.model.spec.ports:
            self.model.spec.ports.remove(p)
        return self


    def _exists_port(self,port):
        for p in self.model.spec.ports:
            if int(p.port)==int(port):
                return True
        return False

class Deploy():

    def __init__(self):
        self.registry_username = self.get_env("KS_DOCKER_REGISTRY_USERNAME")
        self.registry_password = self.get_env("KS_DOCKER_REGISTRY_PASSWORD")
        self.registry = self.get_env('KS_DOCKER_REGISTRY')
        self.project_status = self.get_env("KS_PROJECT_STATUS")
        self.project_name = self.get_env('KS_PROJECT_NAME')
        self.go_pipeline_label = self.get_env("GO_PIPELINE_LABEL")
        self.project_replicas = int(self.get_env("KS_PROJECT_REPLICAS",1))
        self.project_port = int(self.get_env('KS_PROJECT_PORT', 80))
        self.docker_server = self.get_env("KS_DOCKER_SERVER")
        self.k8s_host = self.get_env('K8S_HOST')
        self.container_cpu = self.get_env('KS_CONTAINER_CPU', '2')
        self.container_cpu = self.get_env('KS_CONTAINER_MEMORY', '512M')
        self.k8s_namespace = self.get_env('KS_PROJECT_GROUP',None)

        self.project_branch = self.get_project_branch()
        self.project_commit  = self.get_project_commit()

        self.project_version = '{branch}-{label}.git{commit}'.format(
            branch = self.project_branch,
            label = self.go_pipeline_label,
            commit = self.project_commit
        )

        self.image_name = self.project_name
        self.image_tag = self.project_version
        self.image_tag_name='{image}:{tag}'.format(
            image = self.image_name,
            tag = self.image_tag
        )

        self.k8s_deployment_name = self.project_name + '-' + self.project_status
        self.k8s_image = self.registry + '/' + self.image_name + ':' + self.image_tag

    def connect_docker(self):
        self.dockerClient = Client(base_url=self.docker_server)
        self.dockerClient.login(username=self.registry_username, password=self.registry_password,registry=self.registry)

    def get_project_commit(self):
        commit = commands.getoutput('git log  --pretty=format:"%h" -n 1')
        return commit

    def get_project_branch(self):
        branch = commands.getoutput('git branch | grep "*" | head -n 1')
        branch = re.sub('\*','',branch)
        branch = re.sub("/",".",branch)
        branch = branch.strip()
        log.info(branch)
        return branch

    def get_env(self,key,value=None):
        value = os.getenv(key,value)
        if value == None:
            raise Exception('{key} not be null.'.format(key=key))
        return value

    def build(self, dockerfile='.'):
        self.connect_docker()
        image_tag = self.image_tag_name
        status = True
        log.info('Start To Build Image %s' % image_tag)
        msgs = ''
        for msg in self.dockerClient.build(path=dockerfile, tag=image_tag, forcerm=True,buildargs={'KS_PROJECT_NAME':self.project_name},nocache=True):
            log.info(msg)
            msgs+=msg
            if re.search("error", msg, re.IGNORECASE):
                status = False
        if not re.search("Successfully", msgs, re.IGNORECASE):
            status = False
        else:
            status = True

        if status == True:
            log.info("Build Docker Image[SUCCESS].")
        else:
            log.error("Build Docker Image[FAILD].")
            exit(1)
        return status
    def push(self,image_tag_src=None,image_tag_dest=None):
        self.connect_docker()
        if self.registry=="" or self.registry==None:return
        if image_tag_src == None:image_tag_src= self.image_tag_name
        if image_tag_dest == None:image_tag_dest= self.image_tag_name
        self.dockerClient.login('admin',password='admin123',registry=self.registry)
        self.dockerClient.tag(image_tag_src , repository=self.registry+"/"+self.image_name,tag=self.image_tag)
        response = self.dockerClient.push(repository=self.registry+"/"+image_tag_dest)
        if re.search("ERROR",response,re.IGNORECASE):
            log.error("PUSH IMAGE[%s] TO REPOSITORY FAILD."%image_tag_dest)
            log.error(response)
            exit(1)
        else:
            log.info(response)



    def  deployment_action(self):


        cfg_cert = K8sConfig(kubeconfig=None,auth=('ks_k8s_admin','ks_k8s_pwd'), api_host=self.k8s_host)
        deployment = K8sDeployment(config=cfg_cert, name=self.k8s_deployment_name)
        deployment.add_label(k='project',v=self.project_name)
        if not deployment._exists():
            container = K8sContainer(name=self.k8s_deployment_name, image=self.k8s_image)
            container.add_env('KS_PROJECT_VERSION',self.project_version)
            container.add_image_pull_policy(policy='Always')
            container.add_volume_mount(K8sVolumeMount(name="{project}-resources-volume".format(project=self.k8s_deployment_name),
                                                      mount_path="/data/{project}/resources".format(
                                                          project=self.project_name)))
            #container.add_volume_mount(K8sVolumeMount(name='localtime-volumn',mount_path='/etc/localtime'))
            container.add_volume_mount(K8sVolumeMount(name='{project}-log-volume'.format(project=self.k8s_deployment_name),
                                                      mount_path='/data/logs/'))
            container.add_container_resources_limits(cpu='2', memory='1024Mi')
	    #container.add_container_resources_requests(cpu='200m',memory='512M')
            deployment.add_container(container)
            deployment.add_change_cause('Image Version:{version}'.format(version=self.k8s_image))
            deployment.add_image_pull_secrets([{'name': 'ksszregistrykey'}])

            vol = K8sVolume(name="{project}-resources-volume".format(project=self.k8s_deployment_name), type='hostPath')
            vol.path = "/data/docker/resources/{env}/{project}".format(env=self.project_status,project=self.project_name)
            deployment.add_volume(vol)

            #vol_localtime = K8sVolume(name='localtime-volumn', type='hostPath')
            #vol_localtime.path = "/etc/localtime"
            #deployment.add_volume(vol_localtime)

            vol_log = K8sVolume(name="{project}-log-volume".format(project=self.k8s_deployment_name), type='hostPath')
            vol_log.path = "/data/docker/logs/{env}/{project}".format(env=self.project_status,project=self.project_name)
            deployment.add_volume(vol_log)
            deployment.create()
        else:
            deployment.change_container_resources_limits(cpu='2', memory='1024Mi')
            deployment.set_container_image(name=self.k8s_deployment_name, image=self.k8s_image)
            deployment.add_change_cause('Image Version:{version}'.format(version=self.k8s_image))
            deployment.update()
        deployment.scale(self.project_replicas)

    def service_action(self):
        self.k8s_svc_name = self.project_name+'-'+self.project_status
        cfg_cert = K8sConfig(kubeconfig=None,auth=('ks_k8s_admin','ks_k8s_pwd'), api_host=self.k8s_host)
        service = K8sService(config=cfg_cert, name=self.k8s_svc_name)
        if not service._exists():
            service.add_selector(selector={"name": self.k8s_deployment_name})
            service.type = 'NodePort'
            service.add_port(name=self.k8s_svc_name, port=self.project_port, target_port=self.project_port, protocol='TCP')
            service.create()
        else:

            service.add_selector(selector={"name": self.k8s_deployment_name})
            service.type = 'NodePort'
            if not service._exists_port(self.project_port):
                service.del_port()
                service.add_port(name=self.k8s_svc_name, port=self.project_port, target_port=self.project_port, protocol='TCP')
            service.update()

class PushToProd(Deploy):
    def __init__(self):
        #super(PushToProd,self).__init__()
        Deploy.__init__(self)
        self.prod_registry = self.get_env('KS_PROD_DOCKER_REGISTRY')
        self.prod_registry_username = self.get_env("KS_PROD_DOCKER_REGISTRY_USERNAME")
        self.prod_registry_password = self.get_env("KS_PROD_DOCKER_REGISTRY_PASSWORD")

    def push_to_prod(self):
        image_tag_src= self.image_tag_name
        image_tag_dest= self.image_tag_name
        self.connect_docker()
        self.dockerClient.login(self.registry_username , password=self.registry_password,registry=self.registry)
        self.dockerClient.pull(repository=self.registry+"/"+image_tag_src)

        self.dockerClient.login(self.prod_registry_username,password=self.prod_registry_password,registry=self.prod_registry)
        self.dockerClient.tag(self.registry+"/"+image_tag_src, repository=self.prod_registry + "/" + self.image_name, tag=self.image_tag)
        response = self.dockerClient.push(repository=self.prod_registry + "/" + image_tag_dest)
        if re.search("ERROR", response, re.IGNORECASE):
            log.error("PUSH IMAGE[%s] TO PROD REPOSITORY FAILD." % image_tag_dest)
            log.error(response)
            exit(1)
        else:
            log.info(response)

def main():
    myDeploy = Deploy()
    import argparse
    parser = argparse.ArgumentParser(description='args')

    subparser = parser.add_subparsers(dest='action')
    action_build = subparser.add_parser("build", help="build image")
    action_push = subparser.add_parser("push", help="push image")
    action_deploy = subparser.add_parser("deploy", help="create or update kubernetes deployment")
    action_deploy = subparser.add_parser("svc", help="create or update kubernetes service")
    action_deploy = subparser.add_parser("push2prod", help="push image to prod registry")
    args = parser.parse_args()
    log.info(str(args))
    action = args.action

    if action == 'build':
        myDeploy.build()
    elif action == 'push':
        myDeploy.push()
    elif action == 'deploy':
        myDeploy.deployment_action()
    elif action == 'svc':
        myDeploy.service_action()
    elif action == 'push2prod':
        myPush = PushToProd()
        myPush.push_to_prod()

if __name__=="__main__":
    logging.basicConfig(level = logging.DEBUG)
    main()

