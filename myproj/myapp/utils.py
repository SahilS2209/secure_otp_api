from django.utils import timezone
import re
from rest_framework.response import Response

def get_current_datetime():
    return timezone.now()

def mobile_number_pattern_validation(mobile_number):
        mobile_number_pattern = r'^[6-9]\d{9}$'
        if not re.match(mobile_number_pattern, mobile_number):
            return Response({'error': 'Please provide a valid 10-digit mobile number starting with a digit between 6 and 9.'}, status=400)

def otp_number_pattern_validation(user_otp):
    otp_pattern = r'^\d{6}$'
    if not re.match(otp_pattern, user_otp):
        return Response({'error': 'Please provide a valid 6-digit OTP.'}, status=400)