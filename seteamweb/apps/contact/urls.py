# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.contact import views

urlpatterns = [
    path("list-update", views.contact_list_update, name="customer_append"),
    path("list-api", views.contact_list_api, name="customer_list_api")
]
