from datetime import datetime
import traceback
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, FileResponse, JsonResponse
from django.template import loader
from core import settings
from ..customer.models import Customer
from ..packages.models import Packages
from .models import InspectionSchedule, InspectionRecord, InspectionResultFile, AndroidInspectResult, iOSInspectResult
from .forms import FileUploadForm
from ..utils.utils import edit_inspection_schedule, convertmonth, convert_to_format, convert_datetime, edit_inspection_options
import json
import os

# Create your views here.


def inspect_schedule_list_api(_, schedule, month):
    items = InspectionSchedule.objects.filter(Period=schedule, **{month: True}).values("name")  # 필요한 필드만 추출
    month_int = convertmonth(month)
    results = {"incomplete": "점검 전", "complete": "점검 완료"}
    for item in items:
        try:
            customer = Customer.objects.get(name=item.get('name'))
            inspect_record, is_create = InspectionRecord.objects.get_or_create(customer=customer, inspection_month=month_int)
            item['inspect_result'] = results[inspect_record.result]
            if inspect_record.inspection_date == None:
                item['inspection_date'] = "점검 전"
            else:
                item['inspection_date'] = inspect_record.inspection_date
            item['manager'] = customer.manager.name
            item['inspect_significant'] = inspect_record.details
        except Exception as e:
            print(e)

    return JsonResponse(list(items), safe=False)


def inspection_schedule_edit(request):
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                customer_name = request.POST.get('modify-customer-name')
                month_list = request.POST.getlist('months')
                inspect_period = request.POST.get('inspection-period')
                customer = Customer.objects.get(name=customer_name)
                schedule, _is_create = InspectionSchedule.objects.get_or_create(name=customer)
                edit_inspection_schedule(schedule, month_list, inspect_period)

                return JsonResponse({'status': 'success', "message": "Success"}, status=200)
            else:
                return JsonResponse({"error": "Please check your email and name"}, status=405)

    except Exception as e:
        print(e)
        return JsonResponse({"error": "Please check your email and name"}, status=405)


def inspection_result_append(request):
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                customer_name = Customer.objects.get(name=request.POST.get('customer-name'))
                inspection_month = convert_to_format(request.POST.get('inspect-month'))
                record = InspectionRecord.objects.get(customer=customer_name, inspection_month=inspection_month)
                record.result = 'complete'
                record.inspection_date = convert_datetime(request.POST.get('inspection_date'))
                record.details = request.POST.get('inspect_significant')
                record.save()
                report_title = f"{request.POST.get('title')}.pdf"
                report_file = request.FILES.get('inspection_result_file')
                if report_file:
                    insepction_report, is_create = InspectionResultFile.objects.get_or_create(inspectrecord=record)
                    insepction_report.title = report_title
                    insepction_report.file = report_file
                    insepction_report.save()
                return JsonResponse({'status': 'success', "message": "Success"}, status=200)
            else:
                return JsonResponse({"error": "Please check your email and name"}, status=405)

    except Exception as e:
        print(e)
        return JsonResponse({"error": "Please check your email and name"}, status=405)


def inspection_result_by_app_append(request):
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                platform = request.POST.get('select-platform')
                inspection_date = convert_datetime(request.POST.get('inspection_date'))
                customer = Customer.objects.get(name=request.POST.get('customer-name'))
                package = Packages.objects.get(name=request.POST.get('select_packages'), platform=platform)
                if platform == 'android':
                    result_by_package, is_create = AndroidInspectResult.objects.get_or_create(customer=customer, package=package, inspection_date=inspection_date)
                else:
                    result_by_package, is_create = iOSInspectResult.objects.get_or_create(customer=customer, package=package, inspection_date=inspection_date)
                    result_by_package.library_version = request.POST.get('ios-library-version')
                result_by_package.app_name = request.POST.get('app_name')
                result_by_package.app_version = request.POST.get('app_version')
                result_by_package.significant = request.POST.get('inspect_significant')
                edit_inspection_options(result_by_package, request.POST.getlist('options'), platform)
                result_by_package.save()
                return JsonResponse({'status': 'success', "message": "Success"}, status=200)
            else:
                return JsonResponse({"error": "Please check your email and name"}, status=405)

    except Exception as e:
        print(e)
        return JsonResponse({"error": "Please check your email and name"}, status=405)


def inspection_result_by_app_modify(request):
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                platform = request.POST.get('select-platform')
                inspection_date = convert_datetime(request.POST.get('inspection_date'))
                customer = Customer.objects.get(name=request.POST.get('customer-name'))
                package = Packages.objects.get(name=request.POST.get('select_packages'), platform=platform)
                if platform == 'android':
                    result_by_package = AndroidInspectResult.objects.get(customer=customer, package=package, inspection_date=inspection_date)
                else:
                    result_by_package = iOSInspectResult.objects.get(customer=customer, package=package, inspection_date=inspection_date)
                    result_by_package.library_version = request.POST.get('ios-library-version')
                result_by_package.app_name = request.POST.get('app_name')
                result_by_package.app_version = request.POST.get('app_version')
                result_by_package.significant = request.POST.get('inspect_significant')
                edit_inspection_options(result_by_package, request.POST.getlist('options'), platform)
                result_by_package.save()
                return JsonResponse({'status': 'success', "message": "Success"}, status=200)
            else:
                return JsonResponse({"error": "Please check your email and name"}, status=405)

    except Exception as e:
        print(e)
        traceback.print_exc()
        return JsonResponse({"error": "Please check your email and name"}, status=405)


def inspection_result_by_app_delete(request):
    try:
        if request.method == 'DELETE':
            print(request.GET)
            platform = request.GET.get('platform')
            inspection_date = convert_datetime(request.GET.get('inspectionDate'))
            customer = Customer.objects.get(name=request.GET.get('customerName'))
            package = Packages.objects.get(name=request.GET.get('packageName'), platform=platform)
            if platform == 'android':
                result_by_package = AndroidInspectResult.objects.get(customer=customer, package=package, inspection_date=inspection_date)
            else:
                result_by_package = iOSInspectResult.objects.get(customer=customer, package=package, inspection_date=inspection_date)
            result_by_package.delete()
            return JsonResponse({'status': 'success', "message": "Success"}, status=200)
        else:
            return JsonResponse({"error": "Please check request method"}, status=405)
    except Exception as e:
        print(e)
        traceback.print_exc()
        return JsonResponse({"error": "Please check your email and name"}, status=405)


def inspection_report_view_or_download(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            inspection_month = convert_to_format(data['inspection_month'])
            customer = Customer.objects.get(name=data['customer_name'])
            record = InspectionRecord.objects.get(customer=customer, inspection_month=inspection_month)
            report = InspectionResultFile.objects.get(inspectrecord=record)
            if os.path.exists(report.file.path):
                return FileResponse(open(report.file.path, 'rb'), content_type='application/pdf')
            else:
                return JsonResponse({"error": "Invaild Report File"}, status=405)
        else:
            return JsonResponse({"error": "Please check Method"}, status=405)
    except Exception as e:
        traceback.print_exc()
        print(e)


def inspect_result_by_customer(_, customer_name):
    customer = Customer.objects.get(name=customer_name)
    aos_items = AndroidInspectResult.objects.filter(customer=customer).values()
    ios_items = iOSInspectResult.objects.filter(customer=customer).values()
    for item in aos_items:
        item['platform'] = 'Android'
        item['package_name'] = Packages.objects.get(id=item['package_id']).name
    for item in ios_items:
        item['platform'] = 'iOS'
        item['package_name'] = Packages.objects.get(id=item['package_id']).name
    items = list(aos_items) + list(ios_items)
    items = sorted(items, key=lambda x: x.get('inspection_date') or '', reverse=True)
    return JsonResponse(list(items), safe=False)


def inspect_significant_by_result(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            customer = Customer.objects.get(name=data.get('customer_name'))
            os = "android" if data.get('platform') == 'Android' else "iOS"
            package = Packages.objects.get(name=data.get('package_name'), platform=os)
            if os == 'android':
                item = AndroidInspectResult.objects.get(customer=customer, package=package, inspection_date=data.get('inspection_date'))
            elif os == 'iOS':
                item = iOSInspectResult.objects.get(customer=customer, package=package, inspection_date=data.get('inspection_date'))
            else:
                return JsonResponse({"error": "Please check Platform"}, status=405)
            return JsonResponse({"significant": item.significant}, status=200, json_dumps_params={'ensure_ascii': False, "indent": 2})
        else:
            return JsonResponse({"error": "Please check Method"}, status=405)

    except Exception as e:
        return JsonResponse({"error": e}, status=405)


def inspect_significant_by_monthly_result(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            print(data)
            customer = Customer.objects.get(name=data.get('customer_name'))
            inspection_month = convert_to_format(data['inspection_month'])
            item = InspectionRecord.objects.get(customer=customer, inspection_month=inspection_month)
            return JsonResponse({"significant": item.details}, status=200, json_dumps_params={'ensure_ascii': False, "indent": 2})
        else:
            return JsonResponse({"error": "Please check Method"}, status=405)

    except Exception as e:
        return JsonResponse({"error": e}, status=405)
