# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.inspection import views

urlpatterns = [
    path("list-api/<str:schedule>", views.inspect_schedule_list_api, name="inspect_schedule_list_api"),
    path("delete/<str:item_name>", views.customer_delete, name="customer_delete"),
    path("schedule-modify", views.inspection_schedule_edit, name="inspection_schedule_edit")
]
