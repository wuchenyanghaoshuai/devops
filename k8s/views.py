# _*_ coding: utf-8 _*_
from django.shortcuts import render,redirect
from django.http import  JsonResponse,QueryDict
from  kubernetes import config,client
import os,hashlib,random
from devops import  k8s

# Create your views here.
def node(request):
    return  render(request,'k8s/node.html')


def node_api(request):
    code = 0
    msg = ''
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    k8s.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    if request.method == 'GET':

        search_key=request.GET.get('search_key')
        data=[]
        try:
            for node in core_api.list_node().items:
                print(node.status.capacity['memory'])
                name=node.metadata.name
                labels=node.metadata.labels
                create_time=node.metadata.creation_timestamp
                cpu=node.status.capacity['cpu']
                mem=node.status.capacity['memory']
                print("内存为 %s,cpu为 %s" %(mem,cpu))
                status=node.status.conditions[-1].status
                scheduler=("是" if node.spec.unschedulable is None else "否")
                kubelet_version=node.status.node_info.kubelet_version
                cri_version=node.status.node_info.container_runtime_version
                node={'name':name,'labels':labels,'status':status,'scheduler':scheduler,'cpu':cpu,'memory':mem,'kubelet_version':kubelet_version,'cri_version':cri_version,'create_time':create_time}
                print("下面是打印node信息 %s"%node)
                #根据指定key来进行搜索namespace
                if search_key:
                    if search_key in name:
                        data.append(node)
                else:
                    data.append(node)
                code =0
                msg='获取数据成功'
        except Exception as e:
            print(e)
            code=1
            status=getattr(e,'status')
            if status == 403:
                msg='没有访问权限'
            elif status == 401:
                msg='身份验证失败'
            else:
                msg='获取数据失败'
        count=len(data)
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


def pv(request):
    return  render(request,'k8s/pv.html')

def pv_api(request):
    # 命名空间选择和命名空间表格使用
    code = 0
    msg = ""
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    k8s.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    if request.method == "GET":
        search_key = request.GET.get("search_key")
        data = []
        try:
            for pv in core_api.list_persistent_volume().items:
                name = pv.metadata.name
                capacity = pv.spec.capacity["storage"]
                access_modes = pv.spec.access_modes
                reclaim_policy = pv.spec.persistent_volume_reclaim_policy
                status = pv.status.phase
                if pv.spec.claim_ref is not None:
                    pvc_ns = pv.spec.claim_ref.namespace
                    pvc_name = pv.spec.claim_ref.name
                    pvc = "%s / %s" % (pvc_ns, pvc_name)
                else:
                    pvc = "未绑定"
                storage_class = pv.spec.storage_class_name
                create_time = pv.metadata.creation_timestamp
                pv = {"name": name, "capacity": capacity, "access_modes":access_modes,
                             "reclaim_policy":reclaim_policy , "status":status, "pvc":pvc,
                            "storage_class":storage_class,"create_time": create_time}
                print("下面是打印pv %s" %pv)
                # 根据搜索值返回数据
                if search_key:
                    if search_key in name:
                        data.append(pv)
                else:
                    data.append(pv)
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

        # 分页
        page = int(request.GET.get('page',1))
        limit = int(request.GET.get('limit'))
        start = (page - 1) * limit
        end = page * limit
        data = data[start:end]

        res = {'code': code, 'msg': msg, 'count': count, 'data': data}
        return JsonResponse(res)

    elif request.method == "DELETE":
        request_data = QueryDict(request.body)
        name = request_data.get("name")
        try:
            core_api.delete_persistent_volume(name)
            code = 0
            msg = "删除成功."
        except Exception as e:
            code = 1
            status = getattr(e, "status")
            if status == 403:
                msg = "没有删除权限"
            else:
                msg = "删除失败！"
        res = {'code': code, 'msg': msg}
        return JsonResponse(res)