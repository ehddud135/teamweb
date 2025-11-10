from datetime import datetime
import json
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.template import loader
from apps.inspection.models import AndroidInspectResult, InspectionSchedule, AndroidObfuscateResult
from apps.packages.models import Packages
from django.conf import settings
from apps.automation.models import AndroidResult

# Create your views here.


def package_list_api(request, month):
    month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                  7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
                  }
    inspect_month = month_dict.get(month)
    customers = InspectionSchedule.objects.filter(
        **{inspect_month: True}).values('name__name')
    packages = []
    for customer in customers:
        package = Packages.objects.filter(
            customer__name=customer['name__name'], platform="android").values_list('name', flat=True)
        packages.extend(list(package))
    return JsonResponse(list(packages), safe=False)


@csrf_exempt
def insert_result_api(request):
    token = request.headers.get("X-Api-Key")
    if token != settings.API_KEY:
        return HttpResponseForbidden("Invalid token")
    if request.method == "POST":
        result_data = json.loads(request.body.decode('utf-8'))
        for data in result_data:
            insert_data(data)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)
    return JsonResponse({"status": "success", "message": "Result received"})


def insert_data(data):
    inspection_month = datetime.now().strftime("%Y-%m")
    obfuscation = f"{data['class_metrics']['obfuscated']} / {data['class_metrics']['total']}"
    result, _ = AndroidResult.objects.get_or_create(
        package=Packages.objects.get(
            name=data['package_name'], platform="android"),
        inspection_month=inspection_month
    )
    result.app_name = data['app_info']['name']
    result.app_version = data['app_info']['version']
    result.rooting = data['options']['raw']['CHECK_ROOTING']
    result.integrity = data['options']['raw']['CHECK_INTEGRITY']
    result.emulator = data['options']['raw']['CHECK_EMULATOR']
    result.decompile = data['options']['raw']['PREVENT_DECOMPILE']
    result.obfuscate = obfuscation
    result.momo_size = data['class_metrics']['momo_size']
    result.save()


def result_list_api(request):
    try:
        # results = AndroidResult.objects.annotate(customer_name=F("package__customer"), package_name=F("package__name")).values('customer_name', 'package_name', 'rooting', 'integrity', 'emulator', 'obfuscate', 'momo_size', 'decompile',)
        results = AndroidResult.objects.values(
            'id', 'app_name', 'app_version', 'rooting', 'integrity', 'emulator', 'obfuscate', 'momo_size', 'decompile',)
        return JsonResponse(list(results), safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Please check Server Log"}, status=405)


def delete_api(request, pk):
    context = {}
    try:
        result = get_object_or_404(AndroidResult, pk=pk)
        result.delete()
        return JsonResponse({"status": "success", "message": "Result deleted"})
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def upload_api(request, pk):
    print("test")
    context = {}
    try:
        print(request.method)
        if request.method == "POST":
            result = get_object_or_404(AndroidResult, pk=pk)
            obj = get_result_object(result)
            significant = json.loads(request.body).get('significant')
            obfuscate, _ = AndroidObfuscateResult.objects.get_or_create(
                result=obj)
            obj.app_name = result.app_name
            obj.app_version = result.app_version
            obj.rooting_test = result.rooting
            obj.rooting = result.rooting
            obj.integrity = result.integrity
            obj.emulator = result.emulator
            obj.decompile = result.decompile
            obj.obfuscate = json.loads(request.body).get('isobfuscate')
            obj.significant = significant
            obfuscate.obfuscate = result.obfuscate
            obfuscate.momo_size = result.momo_size
            obfuscate.save()
            obj.save()
            result.delete()
            return JsonResponse({"status": "success", "message": "Result uploaded"})
        else:
            print(request.method)
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

    except Exception as e:
        print(e)
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


def get_result_object(result):
    today = datetime.now().date()
    customer = result.package.customer
    package = result.package
    obj, isCreate = AndroidInspectResult.objects.get_or_create(
        customer=customer, package=package, inspection_date=today)
    if isCreate:
        return obj
    raise Exception("점검결과가 이미 존재합니다. 삭제 후 진행 해주세요.")

def single_inspection(request):
    if request.method == "POST":
        mode = request.POST.get("inspection_mode")
        if mode == "single":
            customer_name = request.POST.get("customer-picker")
            package_name = request.POST.get("package-picker")
            print(customer_name, package_name)
            return JsonResponse({"status": "success", "message": "Single inspection processed"})
        elif mode == "monthly":
            month = datetime.now().month
            print(month)
            return JsonResponse({"status": "success", "message": "Monthly inspection processed"})

        else:
            return JsonResponse({"status": "error", "message": "Invalid inspection mode"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)
