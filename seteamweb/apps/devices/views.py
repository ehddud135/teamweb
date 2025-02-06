from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Devices

# Create your views here.


def devices_list_api(request, os):
    if os == 'iOS':
        items = Devices.objects.filter(os='iOS').values('number', 'name', 'version', 'architecture', 'rooting')
    else:
        items = Devices.objects.filter(os='Android').values('number', 'name', 'version', 'architecture', 'rooting')
    return JsonResponse(list(items), safe=False)
