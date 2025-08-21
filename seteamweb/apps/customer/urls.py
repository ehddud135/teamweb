# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.customer import views

urlpatterns = [
    path("append", views.customer_append, name="customer_append"),
    path("name-list", views.customer_name_list, name="customer_name_list"),
    path("delete/<str:resource>/<str:pk>", views.delete, name="delete"),
    path("installation-record-append", views.installation_record_append, name="installation_record_append"),
    path("view-significant/<str:resource>", views.view_significant, name="view_significant"),
    path("file-fetch/<str:resource>", views.file_fetch, name="file_fetch"),
    path("checklist-append", views.checklist_append, name="checklist_append"),
    path("list-api/<str:resource>", views.list_api, name="list_api"),
]
