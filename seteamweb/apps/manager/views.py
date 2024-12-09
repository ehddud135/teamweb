from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Manager

# Create your views here.


def manager_append(request):
    current_time = datetime.now().date()
    context = {}
    print("method = " + request.method)
    print("content_type = " + request.content_type)
    try:
        if request.method == 'POST':
            if request.content_type == 'multipart/form-data':
                manager_name = request.POST.get("manager-name")
                manager_email = request.POST.get("manager-email")
                if manager_name and manager_email:
                    print("manager_name = " + manager_name)
                    print("manager_email = " + manager_email)
                    print("current_time = " + str(current_time))
                    Manager.objects.create(name=manager_name, email=manager_email)
                    return JsonResponse({'status': 'success', "message": "Success"}, status=200)
                else:
                    return JsonResponse({"error": "Invalid request method"}, status=405)
        return JsonResponse({"error": "Invalid request method"}, status=405)
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def manager_list_api(request):
    items = Manager.objects.values('name', 'email', 'created_at')  # 필요한 필드만 추출
    return JsonResponse(list(items), safe=False)
