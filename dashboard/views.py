from django.shortcuts import render,redirect
from django.http import  JsonResponse,QueryDict
from  kubernetes import config,client
import os,hashlib,random
from devops import  k8s
# Create your views here.
@k8s.self_login_required
def index(request):
    return render(request, 'templates/base.html')

def login(request):
    if request.method == "GET":
        return  render(request, 'login.html')
    elif request.method == "POST":
        token = request.POST.get("token", None)
        if token:
            if k8s.auth_check('token', token):
                request.session['is_login'] = True
                request.session['auth_type'] = 'token'
                request.session['token'] = token
                code = 0
                msg = "认证成功"
            else:
                code = 1
                msg = "Token无效！"
        else:
            file_obj = request.FILES.get("file")
            random_str = hashlib.md5(str(random.random()).encode()).hexdigest()
            file_path = os.path.join('kubeconfig', random_str)
            try:
                with open(file_path, 'w') as f:
                    data = file_obj.read().decode('UTF-8')  # bytes转str
                    f.write(data)
            except Exception as e :
                print(e)
                code = 1
                msg = "文件类型错误！"
            if k8s.auth_check('kubeconfig', random_str):
                request.session['is_login'] = True
                request.session['auth_type'] = 'kubeconfig'
                request.session['token'] = random_str
                code = 0
                msg = "认证成功"
            else:
                code = 1
                msg = "认证文件无效！"
        res = {'code': code, 'msg': msg}
        return JsonResponse(res)


def namespace_api(request):
    code = 0
    msg = ""
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    k8s.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    # 命名空间选择和命名空间表格使用
    if request.method == "GET":
        search_key = request.GET.get("search_key")
        data = []
        try:
            for ns in core_api.list_namespace().items:
                name = ns.metadata.name
                labels = ns.metadata.labels
                create_time = ns.metadata.creation_timestamp
                namespace = {'name':name,'labels':labels,'create_time':create_time}
                # 根据搜索值返回数据
                if search_key:
                    if search_key in name:
                        data.append(namespace)
                else:
                    data.append(namespace)
                code = 0
                msg = "获取数据成功"
        except Exception as e:
            code = 1
            status = getattr(e, "status")
            if status == 403:
                msg = "没有访问权限"
            else:
                msg = "获取数据失败"
        count = len(data)

        #分页
        if request.GET.get('page'):
            page=int(request.GET.get('page',1))
            limit=int(request.GET.get('limit'))
            start=(page-1)*limit
            end=page*limit
            data=data[start:end]
        res={'code':code,'msg':msg,'count':count,'data':data}
        return JsonResponse(res)
    elif request.method =='DELETE':
        request_data=QueryDict(request.body)
        name=request_data.get('name')
        try:
            core_api.delete_namespace(name)
            code =0
            msg='namespace删除成功'
        except Exception as e:
            code=1
            status=getattr(e,'status')
            if status == 403:
                msg='没有删除namespace权限'
            elif status == 401:
                msg='身份验证失败'
            else:
                msg='删除namespace失败'
        res={'code':code,'msg':msg}
        return JsonResponse(res)
    elif request.method == "POST":
        name = request.POST['name']
        # 判断命名空间是否存在
        for ns in core_api.list_namespace().items:
            if name == ns.metadata.name:
                res = {'code': 1, "msg": "命名空间已经存在！"}
                return JsonResponse(res)

        body = client.V1Namespace(
            api_version="v1",
            kind="Namespace",
            metadata=client.V1ObjectMeta(
                name=name
            )
        )
        try:
            core_api.create_namespace(body=body)
            code = 0
            msg = "创建命名空间成功."
        except Exception as e:
            code = 1
            status = getattr(e, "status")
            if status == 403:
                msg = "没有访问权限！"
            else:
                msg = "创建失败！"
        res = {'code': code, 'msg': msg}
        return JsonResponse(res)
def logout(request):
    request.session.flush()
    return redirect(index)

def namespace(request):
    return render(request,'k8s/namespace.html')


def export_resource_api(request):
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    k8s.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()  # namespace,pod,service,pv,pvc
    apps_api = client.AppsV1Api()  # deployment
    networking_api = client.NetworkingV1Api()  # ingress
    storage_api = client.StorageV1Api()  # storage_class

    namespace = request.GET.get('namespace', None)
    resource = request.GET.get('resource', None)
    name = request.GET.get('name', None)
    code = 0
    msg = ""
    result = ""

    import yaml,json
    import yaml,json
    if resource == "namespace":
        try:
            # 坑，不要写py测试，print会二次处理影响结果，到时测试不通
            result = core_api.read_namespace(name=name, _preload_content=False).read()
            result = str(result, "utf-8")  # bytes转字符串
            result = yaml.safe_dump(json.loads(result))  # str/dict -> json -> yaml
        except Exception as e:
            code = 1
            msg = e
    elif resource == "deployment":
        try:
            result = apps_api.read_namespaced_deployment(name=name, namespace=namespace, _preload_content=False).read()
            result = str(result, "utf-8")
            result = yaml.safe_dump(json.loads(result))
        except Exception as e:
            code = 1
            msg = e
    elif resource == "replicaset":
        try:
            result = apps_api.read_namespaced_replica_set(name=name, namespace=namespace, _preload_content=False).read()
            result = str(result, "utf-8")
            result = yaml.safe_dump(json.loads(result))
        except Exception as e:
            code = 1
            msg = e
    elif resource == "daemonset":
        try:
            result = apps_api.read_namespaced_daemon_set(name=name, namespace=namespace, _preload_content=False).read()
            result = str(result, "utf-8")
            result = yaml.safe_dump(json.loads(result))
        except Exception as e:
            code = 1
            msg = e
    elif resource == "statefulset":
        try:
            result = apps_api.read_namespaced_stateful_set(name=name, namespace=namespace,
                                                           _preload_content=False).read()
            result = str(result, "utf-8")
            result = yaml.safe_dump(json.loads(result))
        except Exception as e:
            code = 1
            msg = e
    elif resource == "pod":
        try:
            result = core_api.read_namespaced_pod(name=name, namespace=namespace, _preload_content=False).read()
            result = str(result, "utf-8")
            result = yaml.safe_dump(json.loads(result))
        except Exception as e:
            code = 1
            msg = e
    elif resource == "service":
        try:
            result = core_api.read_namespaced_service(name=name, namespace=namespace, _preload_content=False).read()
            result = str(result, "utf-8")
            result = yaml.safe_dump(json.loads(result))
        except Exception as e:
            code = 1
            msg = e
    elif resource == "ingress":
        try:
            result = networking_api.read_namespaced_ingress(name=name, namespace=namespace,
                                                            _preload_content=False).read()
            result = str(result, "utf-8")
            result = yaml.safe_dump(json.loads(result))
        except Exception as e:
            code = 1
            msg = e
    elif resource == "pvc":
        try:
            result = core_api.read_namespaced_persistent_volume_claim(name=name, namespace=namespace,
                                                                      _preload_content=False).read()
            result = str(result, "utf-8")
            result = yaml.safe_dump(json.loads(result))
        except Exception as e:
            code = 1
            msg = e
    elif resource == "pv":
        try:
            result = core_api.read_persistent_volume(name=name, _preload_content=False).read()
            result = str(result, "utf-8")
            result = yaml.safe_dump(json.loads(result))
        except Exception as e:
            code = 1
            msg = e
    elif resource == "node":
        try:
            result = core_api.read_node(name=name, _preload_content=False).read()
            result = str(result, "utf-8")
            result = yaml.safe_dump(json.loads(result))
        except Exception as e:
            code = 1
            msg = e
    elif resource == "configmap":
        try:
            result = core_api.read_namespaced_config_map(name=name, namespace=namespace, _preload_content=False).read()
            result = str(result, "utf-8")
            result = yaml.safe_dump(json.loads(result))
        except Exception as e:
            code = 1
            msg = e
    elif resource == "storageclass":
        try:
            result = storage_api.read_storage_class(name=name,_preload_content=False).read()
       #     result = core_api.read_namespaced_config_map(name=name, namespace=namespace, _preload_content=False).read()
            result = str(result, "utf-8")
            result = yaml.safe_dump(json.loads(result))
        except Exception as e:
            code = 1
            msg = e
    elif resource == "secret":
        try:
            result = core_api.read_namespaced_secret(name=name, namespace=namespace, _preload_content=False).read()
            result = str(result, "utf-8")
            result = yaml.safe_dump(json.loads(result))
        except Exception as e:
            code = 1
            msg = e

    res = {"code": code, "msg": msg, "data": result}
    return JsonResponse(res)

from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def ace_editor(request):
    d = {}
    namespace = request.GET.get('namespace', None)
    resource = request.GET.get('resource', None)
    name = request.GET.get('name', None)
    d['namespace'] = namespace
    d['resource'] = resource
    d['name'] = name
    return render(request, 'ace_editor.html', {'data': d})