from datetime import datetime
from distutils.util import strtobool
import json
import os
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Customer, Manager, InstallationRecord, InstallationCert, CheckList
from ..packages.models import Packages
from ..inspection.models import InspectionSchedule
from ..utils.utils import convert_datetime, convert_to_format

# Create your views here.


def customer_append(request):
    current_time = datetime.now().date()
    print(request.POST)
    manager = None
    context = {}
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                customer_name = request.POST.get("customer-name")
                customer_manager = request.POST.get("customer-manager")
                is_inspection = bool(strtobool(request.POST.get("inspection_append")))
                if customer_manager:
                    manager = Manager.objects.get(name=customer_manager)
                customer = Customer.objects.create(name=customer_name, manager=manager, inspection=is_inspection)
                if is_inspection == True:
                    InspectionSchedule.objects.create(name=customer)
                return JsonResponse({'status': 'success', "message": "Success"}, status=200)
            else:
                return JsonResponse({"error": "Please check content type"}, status=405)
        return HttpResponse({"error": "Invalid request method"}, status=405)
    except IntegrityError as e:
        return JsonResponse({"error": "Please check customer name<br>고객사명 중복"}, status=405)
    except Exception as e:
        print(e)
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

def customer_name_list(request):
    items = Customer.objects.values('name')
    return JsonResponse(list(items), safe=False)

def delete(request, resource, pk):
    context = {}
    try:
        if request.method == "DELETE":
            if resource == "checklist":
                item = get_object_or_404(CheckList, id=pk)
            elif resource == "installation-record":
                item = get_object_or_404(InstallationRecord, id=pk)
            elif resource == "customer":
                item = get_object_or_404(Customer, name=pk)
            else:
                return JsonResponse({"error": "Invalid resource"}, status=404)
            item.delete()
            return HttpResponse(status=204)  # 성공, 내용 없음 응답
        return HttpResponse("Invalid request method", status=400)
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))



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
                file_name = f"{customer_name}_설치확인서.pdf"
                if file is not None:
                    if file.content_type != 'application/pdf':
                        return JsonResponse({"error": "Please check file type<div> PDF 파일만 업로드 해주세요."}, status=405)
                    InstallationCert.objects.get_or_create(record=record, title=file_name, file=file)
                return JsonResponse({'status': 'success', "message": "Success"}, status=200)
            else:
                return JsonResponse({"error": "Invalid request content type"}, status=405)
        return HttpResponse({"error": "Invalid request method"}, status=405)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Please check Server Log"}, status=405)




def view_significant(request, resource):
    try:
        if request.method == 'POST':
            if resource == "checklist":
                model = CheckList
            elif resource == "installation-record":
                model = InstallationRecord
            else:
                return JsonResponse({"error": "Invalid resource"}, status=404)
            data = json.loads(request.body)
            item = model.objects.get(id=data.get("id"))
            return JsonResponse({"significant": item.significant}, status=200, json_dumps_params={'ensure_ascii': False, "indent": 2})
        else:
            return JsonResponse({"error": "Please check Method"}, status=405)

    except Exception as e:
        return JsonResponse({"error": e}, status=405)




def file_fetch(request, resource):
    try:
        if request.method == 'POST':
            if resource == "installation-cert":
                return get_installation_cert(request)
            elif resource == "checklist":
                return get_checklist_file(request)
            else:
                return JsonResponse({"error": "Invaild Report File"}, status=405)
    except Exception as e:
        print(e)

def get_installation_cert(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            record = InstallationRecord.objects.get(id=data.get("id"))
            report = InstallationCert.objects.get(record=record)
            if os.path.exists(report.file.path):
                return FileResponse(open(report.file.path, 'rb'), content_type='application/pdf', filename=report.title)
            else:
                return JsonResponse({"error": "Invaild Report File"}, status=405)
    except Exception as e:
        print(e)

def get_checklist_file(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            data = CheckList.objects.get(id=data.get("id"))
            if os.path.exists(data.file.path):
                return FileResponse(open(data.file.path, 'rb'), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=data.title)
            else:
                return JsonResponse({"error": "Invaild CheckList File"}, status=405)
    except Exception as e:
        print(e)

def checklist_append(request):
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                print(request.POST)
                customer_name = request.POST.get("customer-picker")
                file = request.FILES.get("checklist-file")
                suffix = os.path.splitext(file.name)[1]
                title = f"{customer_name}_체크리스트{suffix}"
                is_onpremise = bool(strtobool(request.POST.get("isonpremise")))
                significant = request.POST.get("checklist-significant")
                customer = Customer.objects.get(name=customer_name)
                CheckList.objects.create(customer=customer, title=title, file=file, is_onpremise=is_onpremise, significant=significant)
                return JsonResponse({'status': 'success', "message": "Success"}, status=200)
            else:
                return JsonResponse({"error": "Invalid request content type"}, status=405)
        return HttpResponse({"error": "Invalid request method"}, status=405)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Please check Server Log"}, status=405)
    

def list_api(request, resource):
    try:
        if resource == "checklist":
            return get_check_list(request)
        elif resource == "record":
            return get_record_list(request)
        elif resource == "customer":
            return get_customer_list(request)
        else:
            return JsonResponse({"error": "Invalid resource"}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Please check Server Log"}, status=405)


def get_record_list(request):
    try:
        items = InstallationRecord.objects.values('id', 'customer', 'manager', 'installation_date', 'significant')
        for item in items:
            customer = Customer.objects.get(name=item.get('customer'))
            manager = Manager.objects.get(name=item.get('manager'))
            item['customer_name'] = customer.name
            item['manager_name'] = manager.name
        return JsonResponse(list(items), safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Please check Server Log"}, status=405)


def get_customer_list(request):
    try:
        items = Customer.objects.values('id', 'name', 'manager', 'created_at', 'inspection')  # 필요한 필드만 추출
        period_mapping = {
            'monthly': '월',
            'quarter': '분기',
            'half': '반기',
            'undecided': '미정'
        }
        for item in items:
            try:
                customer = Customer.objects.get(name=item.get('name'))
                inspect_schedule = InspectionSchedule.objects.filter(name=customer).first()
                if inspect_schedule is not None:
                    inspect_schedule = period_mapping.get(inspect_schedule.Period, "미정")
                package_count = Packages.objects.filter(customer_id=customer).count()
                item['package_count'] = package_count
                item['inspect_schedule'] = inspect_schedule
            except Exception as e:
                print(e)
        return JsonResponse(list(items), safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Please check Server Log"}, status=405)
    

def get_check_list(request):
    try:
        items = CheckList.objects.values('id', 'customer', 'is_onpremise', 'uploaded_at', 'significant')
        return JsonResponse(list(items), safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Please check Server Log"}, status=405)