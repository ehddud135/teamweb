from datetime import datetime
from ..inspection.models import InspectionSchedule


def convert_datetime(date_str):
    try:
        date_result = datetime.strptime(date_str, "%m/%d/%Y")
        return date_result.date()
    except ValueError:
        return "Invalid date format"


def edit_inspection_schedule(customer, month_list):
    reset_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    print("reset schedule")
    for j in reset_list:
        setattr(customer, j, False)

    for i in month_list:
        setattr(customer, i, True)

    customer.save()
