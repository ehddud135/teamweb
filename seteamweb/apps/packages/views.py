from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Customer, Packages
from apps.utils.utils import convert_datetime

# Create your views here.


def package_append(request):
    context = {}
    print(request.POST)
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                package_name = request.POST.get("package-name")
                customer_name = request.POST.get("customer-name")
                platform = request.POST.get("platform")
                input_date = request.POST.get("license_expire_date")
                license_expire_date = convert_datetime(input_date)
                if customer_name and package_name and platform:
                    customer = Customer.objects.get(name=customer_name)
                    Packages.objects.create(name=package_name, customer=customer, license_expire_date=license_expire_date, platform=platform)
                    return JsonResponse({'status': 'success', "message": "Success"}, status=200)
                else:
                    return JsonResponse({"error": "Please check your email and name"}, status=405)
        return HttpResponse({"error": "Invalid request method"}, status=405)
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def package_list_api(request):
    items = Packages.objects.values('name', 'customer', 'platform', 'license_expire_date', 'created_at')  # 필요한 필드만 추출
    return JsonResponse(list(items), safe=False)


def package_delete(request, item_name, item_platform):
    print(request)
    context = {}
    try:
        if request.method == "DELETE":
            item = get_object_or_404(Packages, name=item_name, platform=item_platform)
            item.delete()
            return HttpResponse(status=204)  # 성공, 내용 없음 응답
        return HttpResponse("Invalid request method", status=400)
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
