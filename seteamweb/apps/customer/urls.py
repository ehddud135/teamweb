# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.customer import views

urlpatterns = [
    path("append", views.customer_append, name="customer_append"),
    path("list-api", views.customer_list_api, name="customer_list_api"),
    path("name-list", views.customer_name_list, name="customer_name_list"),
    path("delete/<str:item_name>", views.customer_delete, name="customer_delete"),
    path("installation-record-append", views.installation_record_append, name="installation_record_append"),
    path("record-list-api", views.record_list_api, name="certificate_list_api"),
    path("view-significant", views.installation_significant, name="installation_significant"),
    path("installation-cert/<str:view_or_download>", views.installation_cert_view_or_download, name="installation_cert_view_or_download"),

]
