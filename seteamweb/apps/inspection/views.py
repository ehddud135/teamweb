from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from ..customer.models import Customer
from ..packages.models import Packages
from .models import InspectionSchedule
from ..utils.utils import edit_inspection_schedule

# Create your views here.

def inspect_schedule_list_api(_, schedule):
    print(schedule)
    items = InspectionSchedule.objects.filter(Period=schedule).values("name")  # 필요한 필드만 추출
    for item in items:
        try:
            customer = Customer.objects.get(name=item.get('name'))
            package_count = Packages.objects.filter(customer_id=customer).count()
            item['package_count'] = package_count
            item['created_at'] = customer.created_at
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
                print(request.POST)
                customer_name = request.POST.get('modify-customer-name')
                month_list = request.POST.getlist('months')
                inspect_period = request.POST.get('inspection-period')
                print(inspect_period)
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
