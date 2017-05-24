import docker
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

logging.basicConfig(level = logging.DEBUG)
client = docker.DockerClient(base_url='tcp://192.168.30.129:5001')
#print client.images.get("registry:latest")
#log.info(client.images.pull("registry:latest"))
log.info(client.images.build())