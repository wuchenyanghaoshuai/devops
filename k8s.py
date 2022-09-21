from kubernetes import config,client
import os,hashlib,random
import json,yaml
#基于token认证

token='eyJhbGciOiJSUzI1NiIsImtpZCI6IllGaVhrMWl1M1daRWlya1B1ZG5IU0ZIZEozV2RnTzdzZmdUazN4MWdQZ0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tMmNkZzYiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiYTQ3ODIzYTYtNGY0MC00YmMzLWE0ZjktYmQxOWM0NWNkYmU5Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmVybmV0ZXMtZGFzaGJvYXJkOmRhc2hib2FyZC1hZG1pbiJ9.tuSxlR-zEcWI2Rn5EmMkYu3VZ1GSVv0LukMvgX1j4qOHoxSUINUZQHkfuvTRmVwnHSPgKeMjoz2NPlQrCIFJ1sOAlgWSAiHuYEta9SVQgPNDVDv5UnRtjGUxD4OvLRfulg2GXP6n9RrjJ_G1P-YDz5_mMwNlIvClewcaVH2oPYQI6YJEG87L5uCbSlBroIV7QPCWyM2g7P-xLbpPo5PWLHQJB6iy3qVRof8Ij2_46Fguf0rzWfOkXzL6g3hHaDWNRXPxuY_nuxv-GpYiQ1O6Agyofv2GrHMoN0GBDop0TBZJDcZWTxfHDUG0GAifLcZ20o2oTHhLZTopfio56JEYwQ'
configuration = client.Configuration()
configuration.host = "https://59.110.152.120:6443" # APISERVER地址
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
# name='test2'
# capacity='50Gi'
# body=client.V1PersistentVolume(
#     api_version="v1",
#     kind="PersistentVolume",
#     metadata=client.V1ObjectMeta(name=name),
#     spec=client.V1PersistentVolumeSpec(
#         capacity={'storage': '50Gi'},
#         access_modes=["ReadWriteOnce"],
#         volume_mode="Filesystem",
#         storage_class_name="managed-nfs-storage",
#         nfs=client.V1NFSVolumeSource(
#             server='192.168.1.1',
#             path='/ifs/kubernetes'
#         ),
#
#     )
# )
#core_api.create_persistent_volume(body=body)

# name='my-pvc-chenyang'
# bodypvc=client.V1PersistentVolumeClaim(
#     api_version="v1",
#     kind="PersistentVolumeClaim",
#     metadata=client.V1ObjectMeta(name=name),
#     spec=client.V1PersistentVolumeClaimSpec(
#         access_modes=["ReadWriteOnce"],
#         storage_class_name='managed-nfs-storage',
#         resources=client.V1ResourceRequirements(
#             requests={"storage":"20Gi"}
#         )
#     )
# )
# try:
#     api_response=core_api.create_namespaced_persistent_volume_claim(namespace='devops',body=bodypvc)
#     print(api_response)
# except Exception as e:
#     print("Exception when calling CoreV1Api->create_namespaced_persistent_volume_claim: %s\n" % e)
labels={"app":"test"}
resources = client.V1ResourceRequirements(limits={"cpu": "4", "memory": "8Gi"},
                                         requests={"cpu": "1", "memory": "2Gi"})
image="nginx:alpine"
body=client.V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name="test-web"),
    spec=client.V1DeploymentSpec(
        replicas=3,
        selector={'matchLabels': {"app":"test"} },
        template=client.V1PodTemplateSpec(

            metadata=client.V1ObjectMeta(labels={"app":"test"}),
            spec=client.V1PodSpec(
                containers=[client.V1Container(
                            name="web",
                            image=image,
                            env=[{"name": "TEST", "value": "123"}, {"name": "DEV", "value": "456"}],
                            ports=[client.V1ContainerPort(container_port=80)],
                            resources=resources,
                        )]
        )
),
    )

)
# client.AppsV1Api().create_namespaced_deployment(namespace="default",body=body)

result=client.AppsV1Api().read_namespaced_deployment(name='test-web',namespace='default',_preload_content=False).read()
result = str(result, "utf-8")
result = yaml.safe_dump(json.loads(result))
print(result)