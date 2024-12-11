from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Customer, Manager

# Create your views here.


def customer_append(request):
    current_time = datetime.now().date()
    context = {}
    print("method = " + request.method)
    print("content_type = " + request.content_type)
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                customer_name = request.POST.get("customer-name")
                customer_manager = request.POST.get("customer-manager")
                if customer_name and customer_manager:
                    print("customer_name = " + customer_name)
                    print("customer_manager = " + customer_manager)
                    print("current_time = " + str(current_time))
                    manager = Manager.objects.get(name=customer_manager)
                    Customer.objects.create(name=customer_name, manager=manager)
                    print("정상 등록 완료")
                    return JsonResponse({'status': 'success', "message": "Success"}, status=200)
                else:
                    return JsonResponse({"error": "Please check your email and name"}, status=405)
        return HttpResponse({"error": "Invalid request method"}, status=405)
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def customer_list_api(request):
    items = Customer.objects.values('name', 'manager', 'created_at')  # 필요한 필드만 추출
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
