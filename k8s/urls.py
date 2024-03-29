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
from k8s import views

urlpatterns = [
    re_path('node/',views.node,name='node'),
    re_path('node_api/$', views.node_api, name='node_api'),
    re_path('node_details/$', views.node_details, name='node_details'),
    re_path('^node_details_pod_list/$', views.node_details_pod_list, name="node_details_pod_list"),
    re_path('pv/',views.pv,name='pv'),
    re_path('pv_api/',views.pv_api,name='pv_api'),
    re_path('pv_create/',views.pv_create,name='pv_create'),

]
