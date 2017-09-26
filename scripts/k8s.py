import time
import kubernetes.client as K8sClient
import kubernetes.config as K8sConfig
from kubernetes.client.rest import ApiException
from pprint import pprint
import demjson
import warnings
warnings.filterwarnings("ignore", category=UnicodeWarning)

K8sClient.configuration.host="192.168.1.10:8080"
api_instance=K8sClient.CoreV1Api()


try:
    api_response_get = api_instance.read_namespaced_service_status("redis-ys-service-blue","default",pretty=True)
    service_blue=(api_response_get.spec.selector["name"])
    service_green='{"spec":{"selector":{"name":"'+service_blue+'"}}}'
    print  service_green
    service_bull_obj=demjson.decode(service_green)
    api_response_patch = api_instance.patch_namespaced_service("redis-ys-service-green","default",service_bull_obj)
#    pprint (api_response_get)
#    print (api_response_get.spec.selector["name"])
#    pprint(api_response_patch)
#    print demjson.encode(str(api_response))
#    dict_json=(demjson.decode(demjson.encode(str(api_response))))
#    api_instance.patch_namespaced_endpoints_with_http_info()
except ApiException as e:
    print("Exception when calling AdmissionregistrationApi->get_api_group: %s\n" % e)

#redis-ys-deployment
#K8sConfig.load_kube_config(config_file=123,persist_config=None)

#cfg_basic = K8sConfig(kubeconfig=None, api_host=somehost:8888, auth=('basic_user', 'basic_passwd'))
# Configure API key authorization: BearerToken
#kubernetes.client.configuration.host = 'http://192.168.1.10:8080'
#kubernetes.client.configuration.api_key['authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# kubernetes.client.configuration.api_key_prefix['authorization'] = 'Bearer'
# create an instance of the API class
# api_instance = kubernetes.client.AdmissionregistrationApi()
#
# try:
#     api_response = api_instance.get_api_group()
#     pprint(api_response)
# except ApiException as e:
#     print("Exception when calling AdmissionregistrationApi->get_api_group: %s\n" % e)