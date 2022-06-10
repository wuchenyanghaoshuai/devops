from django.shortcuts import render,redirect
from django.http import  JsonResponse
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
            print(token)
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
                    print(type(data))
                    print(data)
                    f.write(data)
            except Exception as e :
                print(e)
                code = 1
                msg = "文件类型错误！"
            if k8s.auth_check('kubeconfig', random_str):
                print('random_str: %s' %random)
                request.session['is_login'] = True
                request.session['auth_type'] = 'token'
                request.session['token'] = random_str
                print('random_str: %s'%random_str)
                code = 0
                msg = "认证成功"
            else:
                code = 1
                msg = "认证文件无效！"
        res = {'code': code, 'msg': msg}
        return JsonResponse(res)



def namespace_api(request):
    if request.method == 'GET':
        code =0
        msg=''
        auth_type= request.session.get('auth_type')
        token=request.session.get('token')
        print("=======")
        print(auth_type,token)
        k8s.load_auth_config(auth_type,token)
        core_api=client.CoreV1Api()
        data=[]
        try:
            for ns in core_api.list_namespace().items:
                name=ns.metadata.name
                labels=ns.metadata.labels
                create_time=ns.metadata.creation_timestamp
                print(ns.metadata.name)
                namespace={'name':name,'labels':labels,'create_time':create_time}
                data.append(namespace)
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
        res={'code':code,'msg':msg,'count':count,'data':data}
        return JsonResponse(res)


def logout(request):
    request.session.flush()
    return redirect(index)