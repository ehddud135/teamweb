# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.devices import views

urlpatterns = [
    # path("append", views.package_append, name="package_append"),
    path("list-api/<str:os>", views.devices_list_api, name="devices_list_api")
    # path("delete/<str:item_name>/<str:item_platform>", views.package_delete, name="package_delete"),
    # path("list-by-cusomter-api/<str:customer_name>/<str:platform>", views.package_list_by_customer, name="package_list_by_customer")
]
