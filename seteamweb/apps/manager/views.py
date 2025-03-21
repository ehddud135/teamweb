from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Manager
from ..customer.models import Customer

# Create your views here.


def manager_append(request):
    current_time = datetime.now().date()
    context = {}
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                manager_name = request.POST.get("manager-name")
                manager_email = request.POST.get("manager-email")
                if manager_name and manager_email:
                    Manager.objects.create(name=manager_name, email=manager_email)
                    return JsonResponse({'status': 'success', "message": "Success"}, status=200)
                else:
                    return JsonResponse({"error": "Please check your email and name"}, status=405)
        return HttpResponse({"error": "Invalid request method"}, status=405)
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def manager_list_api(request):
    items = Manager.objects.values('name', 'email', 'created_at')  # 필요한 필드만 추출
    for item in items:
        try:
            manager = Manager.objects.get(name=item.get('name'))
            custoemr_count = Customer.objects.filter(manager_id=manager).count()
            item['customer_count'] = custoemr_count
        except Exception as e:
            print(e)
    return JsonResponse(list(items), safe=False)


def manager_delete(request, item_name):
    context = {}
    try:
        if request.method == "DELETE":
            item = get_object_or_404(Manager, name=item_name)
            item.delete()
            return HttpResponse(status=204)  # 성공, 내용 없음 응답
        return HttpResponse("Invalid request method", status=400)
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
