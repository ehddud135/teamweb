# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.dashboard import views

urlpatterns = [
    path("monthly-customer-count", views.monthly_customer_count, name="monthly_customer_count"),
    path("inspection-customer-count", views.inspection_customer_count, name="inspection_customer_count"),
]
