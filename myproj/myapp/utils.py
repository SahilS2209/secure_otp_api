import re
from django.utils import timezone

def get_current_datetime():
    return timezone.now()

def validate_mobile_number(mobile_number):
    pattern = r'^[6-9]\d{9}$'
    return bool(re.match(pattern, mobile_number))