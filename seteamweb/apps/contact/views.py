from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Organization, Contact, ContactEmail, Label
from ..utils.EmailContactsList import EmailContactsList

# Create your views here.


def contact_list_update(request):
    try:
        if request.method == 'POST':
            em = EmailContactsList()
            contact_list = em.get_data()
            for contact in contact_list:
                organization, is_create = Organization.objects.get_or_create(name=contact['Organization'])
                contact_obj, is_create = Contact.objects.get_or_create(name=contact['Name'], organization=organization)
                for email in contact['Email'].split(", "):
                    ContactEmail.objects.get_or_create(contact=contact_obj, email=email)
                for label in contact['Labels'].split(", "):
                    label_obj, is_create = Label.objects.get_or_create(name=label, google_id=label)
                    label_obj.contacts.add(organization)

            return JsonResponse({'status': 'success', "message": "Success"}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'failed', "message": "failed"}, status=404)


def contact_list_api(request):
    print("Test")
    try:
        print("Test2")
    except Exception as e:
        print(e)
    #     period_mapping = {
    #         'monthly': '월',
    #         'quarter': '분기',
    #         'half': '반기',
    #         'undecided': '미정'
    #     }
    #     for item in items:
    #         try:
    #             inspect_schedule, is_create = InspectionSchedule.objects.get_or_create(name=customer)
    #             inspect_schedule = period_mapping.get(inspect_schedule.Period, "미정")
    #             package_count = Packages.objects.filter(customer_id=customer).count()
    #             item['package_count'] = package_count
    #             item['inspect_schedule'] = inspect_schedule
    #         except Exception as e:
    #             print(e)

    return JsonResponse("", safe=False)
