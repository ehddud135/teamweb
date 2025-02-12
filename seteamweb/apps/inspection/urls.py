# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.inspection import views

urlpatterns = [
    path("list-api/<str:schedule>/<str:month>", views.inspect_schedule_list_api, name="inspect_schedule_list_api"),
    path("result-by-customer/<str:customer_name>", views.inspect_result_by_customer, name="inspect_result_by_customer"),
    path("delete/<str:item_name>", views.customer_delete, name="customer_delete"),
    path("schedule-modify", views.inspection_schedule_edit, name="inspection_schedule_edit"),
    path("result-append", views.inspection_result_append, name="inspection_result_append"),
    path("result-by-app-append", views.inspection_result_by_app_append, name="inspection_result_by_app_append"),
    path("report/<str:view_or_download>", views.inspection_report_view_or_download, name="inspection_report_view"),
    path("significant-per-app", views.inspect_significant_by_result, name="inspect_significant_by_result")

]
