from datetime import datetime
import json
import os
from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Customer, Manager, InstallationRecord, InstallationCert
from ..packages.models import Packages
from ..inspection.models import InspectionSchedule
from ..utils.utils import convert_datetime, convert_to_format

# Create your views here.


def customer_append(request):
    current_time = datetime.now().date()
    inspection = False
    context = {}
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                customer_name = request.POST.get("customer-name")
                customer_manager = request.POST.get("customer-manager")
                if request.POST.get("inspection"):
                    inspection = True
                if customer_name and customer_manager:
                    manager = Manager.objects.get(name=customer_manager)
                    Customer.objects.create(name=customer_name, manager=manager, inspection=inspection)
                    return JsonResponse({'status': 'success', "message": "Success"}, status=200)
                else:
                    return JsonResponse({"error": "Please check your email and name"}, status=405)
        return HttpResponse({"error": "Invalid request method"}, status=405)
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def customer_list_api(_):
    items = Customer.objects.values('name', 'manager', 'created_at', 'inspection')  # 필요한 필드만 추출
    period_mapping = {
        'monthly': '월',
        'quarter': '분기',
        'half': '반기',
        'undecided': '미정'
    }
    for item in items:
        try:
            customer = Customer.objects.get(name=item.get('name'))
            inspect_schedule, is_create = InspectionSchedule.objects.get_or_create(name=customer)
            inspect_schedule = period_mapping.get(inspect_schedule.Period, "미정")
            package_count = Packages.objects.filter(customer_id=customer).count()
            item['package_count'] = package_count
            item['inspect_schedule'] = inspect_schedule
        except Exception as e:
            print(e)

    return JsonResponse(list(items), safe=False)


def customer_name_list(request):
    items = Customer.objects.values('name')
    return JsonResponse(list(items), safe=False)


def customer_delete(request, item_name):
    context = {}
    try:
        if request.method == "DELETE":
            item = get_object_or_404(Customer, name=item_name)
            item.delete()
            return HttpResponse(status=204)  # 성공, 내용 없음 응답
        return HttpResponse("Invalid request method", status=400)
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def record_list_api(request):
    try:
        items = InstallationRecord.objects.values('customer', 'manager', 'installation_date', 'significant')  # 필요한 필드만 추출
        for item in items:
            customer = Customer.objects.get(name=item.get('customer'))
            manager = Manager.objects.get(name=item.get('manager'))
            item['customer_name'] = customer.name
            item['manager_name'] = manager.name
        return JsonResponse(list(items), safe=False)
    except Exception as e:
        print(e)


def installation_record_append(request):
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                customer_name = request.POST.get("customer-picker")
                installation_date = request.POST.get("installation-date")
                manager_name = request.POST.get("manager-picker")
                manager = Manager.objects.get(name=manager_name)
                customer = Customer.objects.get(name=customer_name)
                significant = request.POST.get("installation-significant")
                record, is_create = InstallationRecord.objects.get_or_create(customer=customer, manager=manager, installation_date=convert_datetime(installation_date), significant=significant)
                file = request.FILES.get("installation-record-file")
                if file is not None:
                    file_name = file.name.split(".")[-1]
                    if file_name not in ['pdf']:
                        return JsonResponse({"error": "Invalid file type"}, status=405)
                    InstallationCert.objects.create(record=record, title=file.name, file=file)
                return JsonResponse({'status': 'success', "message": "Success"}, status=200)
            else:
                return JsonResponse({"error": "Invalid request content type"}, status=405)
        return HttpResponse({"error": "Invalid request method"}, status=405)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Please check Server Log"}, status=405)


def installation_significant(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            item = InstallationRecord.objects.get(customer=data.get("customer_name"), installation_date=data.get('installation_date'))
            return JsonResponse({"significant": item.significant}, status=200, json_dumps_params={'ensure_ascii': False, "indent": 2})
        else:
            return JsonResponse({"error": "Please check Method"}, status=405)

    except Exception as e:
        return JsonResponse({"error": e}, status=405)


def installation_cert_view_or_download(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            record = InstallationRecord.objects.get(customer=data.get("customer_name"), installation_date=data.get('installation_date'))
            report = InstallationCert.objects.get(record=record)
            if os.path.exists(report.file.path):
                return FileResponse(open(report.file.path, 'rb'), content_type='application/pdf')
            else:
                return JsonResponse({"error": "Invaild Report File"}, status=405)
    except Exception as e:
        print(e)
