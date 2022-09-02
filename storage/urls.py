from django.contrib import admin
from django.urls import path,re_path,include
from storage import views

urlpatterns = [
    re_path('pvc/',views.pvc,name='pvc'),
    re_path('pvc_api/',views.pvc_api,name='pvc_api'),
    re_path('configmap/', views.configmap, name='configmap'),
    re_path('configmap_api/', views.configmap_api, name='configmap_api'),
    re_path('secret/', views.secret, name='secret'),
    re_path('secret_api/', views.secret_api, name='secret_api'),
    re_path('pv_storage/', views.pv_storage, name='pv_storage'),
    re_path('pv_storage_api/', views.pv_storage_api, name='pv_storage_api'),
    re_path('storageclass/', views.storageclass, name='storageclass'),
    re_path('storageclass_api/', views.storageclass_api, name='storageclass_api'),
]
