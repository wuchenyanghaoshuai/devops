from kubernetes import config,client
import os,hashlib,random
import json
#基于token认证


token='eyJhbGciOiJSUzI1NiIsImtpZCI6Ik83MWM5YllYU2c4ZHg3Y3puZk5oUW1xcUppeXFZVTlrTVZZTEllcnRGVVUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tZ3ptd3giLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiOGJkYjdhOTgtZDU5Zi00NTQ0LTg4NjUtMTIzN2Q2NDQzYzlhIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmVybmV0ZXMtZGFzaGJvYXJkOmRhc2hib2FyZC1hZG1pbiJ9.gm2BrgRzGdEI-xI5fp97OsCAyU25DZTgJr5EXPHAOJBEWmX9PbEj_CCOvz1cF59cVYZWJuYj8soJgnTSjS31q6lRN9qoQS-P19VSMtkdqUmzAl2A4U2Da7d1Kta1LMU_CVBddoVAy_m1yfVLcUjs-FPq_55tV54-LwONhwWnPljFpR83dDKhk7tJzthLMkYZv0saPE44TFGgrRRfh_WMeELgbgVEgYJKjzFeE_OHgWILG-bYKmJJzAldRYoF0yis3xxbD8l0iXivQdrBH61ghXiIhesspm68QI6zF03AKpvPGVC9y5G1mV5zYyVj2IL2afKs8icM1GaIfOTlWxo1QQ'
configuration = client.Configuration()
configuration.host = "https://8.142.112.60:6443" # APISERVER地址
configuration.ssl_ca_cert = "/Users/wuchenyang/code/devops/kubeconfig/ca.crt"  # CA证书
configuration.verify_ssl = True  # 启用证书验证
configuration.api_key = {"authorization": "Bearer " + token}  # 指定Token字符串
client.Configuration.set_default(configuration)
sc_v1=client.StorageV1Api()
apps_v1=client.AppsV1Api()
core_api = client.CoreV1Api()
# for i in apps_v1.list_namespaced_deployment(namespace='default').items:
#     print(i.metadata.name)

print("===========")
for sc in sc_v1.list_storage_class().items:
    print(sc.metadata.name)
    print(sc.provisioner)
    print(sc.reclaim_policy)
    print(sc.volume_binding_mode)
    print(sc.allow_volume_expansion)
    print(sc.metadata.creation_timestamp)
    # print("==========1===========")
    #
    # print("===========2===========")
    # print(sc.metadata.managed_fields)
print("===========")
# for pv in core_api.list_persistent_volume().items:
#     print(pv.metadata.name)
#     print(pv.spec.capacity['storage'])