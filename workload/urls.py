"""devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from workload import views

urlpatterns = [
    re_path('deployment/',views.deployment,name='deployment'),
    re_path('deployment_api/',views.deployment_api,name='deployment_api'),
    re_path('deployment_create/',views.deployment_create,name='deployment_create'),
    re_path('^deployment_details/$', views.deployment_details, name="deployment_details"),
    re_path('^replicaset_api/$', views.replicaset_api, name="replicaset_api"),
    re_path('daemonset/', views.daemonset, name='daemonset'),
    re_path('daemonset_api/', views.daemonset_api, name='daemonset_api'),
    re_path('statefulset/', views.statefulset, name='statefulset'),
    re_path('statefulset_api/', views.statefulset_api, name='statefulset_api'),
    re_path('pod/', views.pod, name='pod'),
    re_path('pod_api/', views.pod_api, name='pod_api'),
    re_path('^pod_log/$', views.pod_log, name="pod_log"),
    re_path('^terminal/$', views.terminal, name="terminal"),
]
