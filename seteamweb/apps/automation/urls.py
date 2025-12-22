# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.automation import views

urlpatterns = [
    path("list-api", views.result_list_api, name="result_list_api"),
    path("package-list-api/<int:month>", views.package_list_api, name="package_list_api"),
    path("insert-result-api", views.insert_result_api, name="insert_result_api"),
    path("delete/<str:pk>", views.delete_api, name="delete_api"),
    path("upload/<str:pk>", views.upload_api, name="upload_api"),
    path("inspection-request", views.single_inspection, name="single_inspection"),
    path("delete-previous-results", views.delete_previous_results, name="delete_previous_results"),
]
