# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.devices import views

urlpatterns = [
    path("list-api/<str:os>", views.devices_list_api, name="devices_list_api")
]
