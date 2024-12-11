from datetime import datetime


def convert_datetime(date_str):
    try:
        date_result = datetime.strptime(date_str, "%m/%d/%Y")
        return date_result.date()
    except ValueError:
        return "Invalid date format"
