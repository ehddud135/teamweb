from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Customer, Manager
from ..packages.models import Packages
from ..inspection.models import InspectionSchedule

# Create your views here.


def customer_append(request):
    current_time = datetime.now().date()
    context = {}
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                customer_name = request.POST.get("customer-name")
                customer_manager = request.POST.get("customer-manager")
                if customer_name and customer_manager:
                    manager = Manager.objects.get(name=customer_manager)
                    Customer.objects.create(name=customer_name, manager=manager)
                    return JsonResponse({'status': 'success', "message": "Success"}, status=200)
                else:
                    return JsonResponse({"error": "Please check your email and name"}, status=405)
        return HttpResponse({"error": "Invalid request method"}, status=405)
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def customer_list_api(_):
    items = Customer.objects.values('name', 'manager', 'created_at')  # 필요한 필드만 추출
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
