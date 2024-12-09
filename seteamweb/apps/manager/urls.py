# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.manager import views

urlpatterns = [
    path("append", views.manager_append, name="manager_append"),
    path("list-api", views.manager_list_api, name="manager_list_api")
]
