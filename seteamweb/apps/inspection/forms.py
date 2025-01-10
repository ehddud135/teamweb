# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from .models import InspectionResultFile


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = InspectionResultFile
        fields = ['inspectrecord','title', 'file']

