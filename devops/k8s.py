from kubernetes import client,config
from django.shortcuts import redirect
import os
#登录认证检查
def auth_check(auth_type, str):
    if auth_type == "token":
        token = str
        configuration = client.Configuration()
        configuration.host = "https://59.110.152.120:6443"  # APISERVER地址
        configuration.ssl_ca_cert = os.path.join('kubeconfig', 'ca.crt')
        configuration.verify_ssl = True  # 启用证书验证
        configuration.api_key = {"authorization": "Bearer " + token}  # 指定Token字符串
        client.Configuration.set_default(configuration)
        try:
            core_api = client.CoreApi()
            core_api.get_api_versions()  # 查询资源测试
            return True
        except Exception as e:
            print(e)
            return False
    elif auth_type == "kubeconfig":
        random_str = str
        file_path = os.path.join('kubeconfig', random_str)
        config.load_kube_config(r"%s" % file_path)
        try:
            core_api = client.CoreApi()
            core_api.get_api_versions()  # 查询资源测试
            return True
        except Exception:
            return False

#登录认证装饰器
def self_login_required(func):
    def inner(request,*args,**kwargs):
        is_login=request.session.get('is_login',False)
        if is_login:
            return func(request,*args,**kwargs)
        else:
            return redirect('/login')
    return inner




#加载认证配置
def load_auth_config(auth_type,str):
    if auth_type =='token':
        token = str
        configuration = client.Configuration()
        configuration.host = "https://59.110.152.120:6443"  # APISERVER地址
        configuration.ssl_ca_cert = r"%s" %(os.path.join('kubeconfig', "ca.crt"))
        configuration.verify_ssl = True  # 启用证书验证
        configuration.api_key = {"authorization": "Bearer " + token}  # 指定Token字符串
        client.Configuration.set_default(configuration)
    elif auth_type =='kubeconfig':
        random_str = str
        file_path = os.path.join('kubeconfig', random_str)
        print('下面是file_path%s'%file_path)
        config.load_kube_config(r"%s"  %file_path)

#时间戳格式化
from datetime import  date,timedelta
def datetime_format(timestamp):
    t=date.strftime((timestamp + timedelta(hours=8)),'%Y-%m-%d %H:%M:%S')
    return t
from datetime import date,timedelta
def dt_format(timestamp):
    t = date.strftime((timestamp + timedelta(hours=8)), '%Y-%m-%d %H:%M:%S')
    return t