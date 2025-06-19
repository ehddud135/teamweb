from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from ..inspection.models import InspectionSchedule
from ..customer.models import Customer

# Create your views here.


def monthly_customer_count(request):
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    month_counts = {}

    for month in months:
        count = InspectionSchedule.objects.filter(**{month: True}).count()
        month_counts[month] = count

    return JsonResponse(month_counts)


# def customer_count_by_manager(request):
#     managers = InspectionSchedule.objects.values_list('name__manager__name', flat=True).distinct()
#     manager_counts = {}

#     for manager in managers:
#         count = InspectionSchedule.objects.filter(name__manager__name=manager).count()
#         manager_counts[manager] = count

#     return JsonResponse(manager_counts)

def inspection_customer_count(request):
    custoemr_counts = {}
    all_custeomers = Customer.objects.all().count()
    inspection_customers = Customer.objects.filter(inspection=True).count()
    custoemr_counts["all_custeomers"] = all_custeomers
    custoemr_counts["inspection_customers"] = inspection_customers
    print(all_custeomers)
    print(inspection_customers)
    return JsonResponse(custoemr_counts)
