from kubernetes import config,client
import os,hashlib,random
#基于https证书
config.load_kube_config(r'C:\Users\chenyang\PycharmProjects\devops\config')
apps_v1=client.AppsV1Api()
for i in apps_v1.list_namespaced_deployment(namespace='default').items:
    print(i.metadata.name)
print('============分隔符================')
#基于token认证
token='eyJhbGciOiJSUzI1NiIsImtpZCI6IlhCcnQ2S3VxNmMwWTJXblJlUlpEYWdMcmdXREFEcmNzR25EVk1pSUxxeDAifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tdjV2YnAiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiYzZjMzRhZmEtOGI0Yi00NTc5LThkODMtY2IzYzYyNzE0MjJiIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmVybmV0ZXMtZGFzaGJvYXJkOmRhc2hib2FyZC1hZG1pbiJ9.nw_47iQT6sPfLkExpR1Su6Vm6RyfO5jHE4ICHFXEUx3p6OxAo4WFhMngZeeDeCfe76gqTIe6TnxnYcI4cHdnY2nwgZ0tMTgF2H-SHCAKOZ9KSGvYtylzDmahQnM5U8XtKQMAICt260eqy1hnryinM5sLs2b0d2yVBydiE5szmAW2MZmK348jL3YDlaDUTA8N63V7Kw2AOqpw3fnoa5od6Tb02jyV_m9qq_Yhjz1Pc0rX0MBt4d45VBIXEBXnG33rOQAbOawVAfZuuIHMlaVFRllhg2udD4IwAerb6rn4D0_4Qo7E2Pr2RopMLMWgqFqEHdZH5NiOIL5gw4XMdcQ8eg'
configuration = client.Configuration()
configuration.host = "https://8.142.204.130:6443"  # APISERVER地址
configuration.ssl_ca_cert = r"C:\Users\chenyang\PycharmProjects\devops\ca.crt"  # CA证书
configuration.verify_ssl = True  # 启用证书验证
configuration.api_key = {"authorization": "Bearer " + token}  # 指定Token字符串
client.Configuration.set_default(configuration)
apps_v1=client.AppsV1Api()
for i in apps_v1.list_namespaced_deployment(namespace='default').items:
    print(i.metadata.name)

print('============分隔符================')
random_str=hashlib.md5(str(random.random()).encode()).hexdigest()
file_path=os.path.join('kubeconfig',random_str)

print(file_path)
print('============分隔符================')
config.load_kube_config(r'C:\Users\chenyang\PycharmProjects\devops\kubeconfig\b3b19cc5b2b97106b18246564f099bf0')  # 使用k8s来校验证书是否可用
#core_api = client.CoreApi()
core_api=client.CoreV1Api()
# print(core_api.get_api_versions())
for ns in core_api.list_namespace().items:
    print(ns.metadata.name)