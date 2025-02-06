from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, FileResponse, JsonResponse
from django.template import loader
from core import settings
from ..customer.models import Customer
from ..packages.models import Packages
from .models import InspectionSchedule, InspectionRecord, InspectionResultFile, AndroidInspectResult, iOSInspectResult
from .forms import FileUploadForm
from ..utils.utils import edit_inspection_schedule, convertmonth, convert_to_format, convert_datetime
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
        except Exception as e:
            print(e)

    return JsonResponse(list(items), safe=False)


def customer_delete(request, item_name):
    print(request)
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


def inspection_schedule_edit(request):
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                customer_name = request.POST.get('modify-customer-name')
                month_list = request.POST.getlist('months')
                inspect_period = request.POST.get('inspection-period')
                customer = Customer.objects.get(name=customer_name)
                schedule, is_create = InspectionSchedule.objects.get_or_create(name=customer)
                if is_create == True:
                    print("새 스케쥴 생성")
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
                print(request.POST)
                customer_name = Customer.objects.get(name=request.POST.get('customer-name'))
                inspection_month = convert_to_format(request.POST.get('inspect-month'))
                customer = InspectionRecord.objects.get(customer=customer_name, inspection_month=inspection_month)
                customer.result = 'complete'
                customer.inspection_date = convert_datetime(request.POST.get('inspection_date'))
                customer.details = request.POST.get('inspect_significant')
                customer.save()
                report_title = f"{request.POST.get('title')}.pdf"
                report_file = request.FILES.get('inspection_result_file')
                insepction_report, is_create = InspectionResultFile.objects.get_or_create(inspectrecord=customer)
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
                print(request.POST)
                customer = Customer.objects.get(name=request.POST.get('customer-name'))
                package = Packages.objects.get(name=request.POST.get('package-name'))
                # customer_name = Customer.objects.get(name=request.POST.get('customer-name'))
                # inspection_month = convert_to_format(request.POST.get('inspect-month'))
                # customer = InspectionRecord.objects.get(customer=customer_name, inspection_month=inspection_month)
                # customer.result = 'complete'
                # customer.inspection_date = convert_datetime(request.POST.get('inspection_date'))
                # customer.details = request.POST.get('inspect_significant')
                # customer.save()
                # report_title = f"{request.POST.get('title')}.pdf"
                # report_file = request.FILES.get('inspection_result_file')
                # insepction_report, is_create = InspectionResultFile.objects.get_or_create(inspectrecord=customer)
                # insepction_report.title = report_title
                # insepction_report.file = report_file
                # insepction_report.save()
                return JsonResponse({'status': 'success', "message": "Success"}, status=200)
            else:
                return JsonResponse({"error": "Please check your email and name"}, status=405)

    except Exception as e:
        print(e)
        return JsonResponse({"error": "Please check your email and name"}, status=405)


def inspection_report_view_or_download(request, view_or_download):
    try:
        if request.method == 'POST':
            print(view_or_download)
            data = json.loads(request.body)
            inspection_month = convert_to_format(data['inspection_month'])
            customer = Customer.objects.get(name=data['customer_name'])
            customer = InspectionRecord.objects.get(customer=customer, inspection_month=inspection_month)
            report = InspectionResultFile.objects.get(inspectrecord=customer)
            if os.path.exists(report.file.path):
                return FileResponse(open(report.file.path, 'rb'), content_type='application/pdf')
            else:
                return JsonResponse({"error": "Invaild Report File"}, status=405)
    except Exception as e:
        print(e)


def inspect_result_by_customer(_, customer_name):
    customer = Customer.objects.get(name=customer_name)
    aos_items = AndroidInspectResult.objects.filter(customer=customer)
    ios_items = iOSInspectResult.objects.filter(customer=customer)  # 필요한 필드만 추출
    # month_int = convertmonth(month)
    # for item in items:
    #     try:
    #         customer = Customer.objects.get(name=item.get('name'))
    #         inspect_record, is_create = InspectionRecord.objects.get_or_create(customer=customer, inspection_month=month_int)
    #         item['inspect_result'] = results[inspect_record.result]
    #         if inspect_record.inspection_date == None:
    #             item['inspection_date'] = "점검 전"
    #         else:
    #             item['inspection_date'] = inspect_record.inspection_date
    #         item['manager'] = customer.manager.name
    #     except Exception as e:
    #         print(e)

    return JsonResponse(list(aos_items), safe=False)
