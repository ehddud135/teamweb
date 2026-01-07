
import re
import os
from datetime import datetime
from django.core.exceptions import ValidationError


def convert_datetime(date_str):
    try:
        date_result = datetime.strptime(date_str, "%m/%d/%Y")
        return date_result.date()
    except ValueError:
        return "Invalid date format"


def edit_inspection_schedule(customer, month_list, inspect_period):
    reset_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    setattr(customer, "Period", inspect_period)
    for j in reset_list:
        setattr(customer, j, False)

    for i in month_list:
        setattr(customer, i, True)

    customer.save()


def edit_inspection_options(result, options_list, platform):
    ios_option_list = ['jailbreak_test', 'jailbreak', 'integrity', 'string_encrypt', 'symbol_del']
    android_option_list = ['rooting_test', 'rooting', 'integrity', 'emulator', 'obfuscate', 'decompile']
    if platform == 'iOS':
        for i in ios_option_list:
            setattr(result, i, False)
        for i in options_list:
            setattr(result, i, True)
    else:
        for i in android_option_list:
            setattr(result, i, False)
        for i in options_list:
            setattr(result, i, True)


def convertmonth(month_full_string):
    match = re.match(r'(\d{4})년\s(\d{1,2})월', month_full_string)
    month = match.group(2)
    months = {
        '01' : "January",
        '02' : "February",
        '03' : "March",
        '04' : "April",
        '05' : "May",
        '06' : "June",
        '07' : "July",
        '08' : "August",
        '09' : "September",
        '10' : "October",
        '11' : "November",
        '12' : "December",
    }
    return months[month]


def validate_year_month(value):
    if not re.match(r'^\d{4}-(0[1-9]|1[0-2])$', value):
        raise ValidationError('%s 는 올바른 형식이 아닙니다.' % value)


def convert_to_format(date_string):
    import re
    match = re.match(r'(\d{4})년\s(\d{1,2})월', date_string)
    if match:
        year = match.group(1)
        month = int(match.group(2))
        return f"{year}-{month:02d}"
    return None
