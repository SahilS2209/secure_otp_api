from rest_framework.decorators import api_view
from rest_framework.response import Response
from .constants import MAX_COUNT_MOBILENO
from .services import OTPService
import base64
from .serializers import VerifyOTPSerializer
from .utils import mobile_number_pattern_validation, otp_number_pattern_validation

otp_requests_counter={}
otp_requests_counter['counter']=1


@api_view(['POST'])
def request_otp_view(request):
    ip_address=request.META.get('REMOTE_ADDR')
    mobile_number_base64 = request.data.get('mobile_number')
    try:
        mobile_number = base64.b64decode(mobile_number_base64).decode('utf-8')
    except:
        return Response({'error': 'Invalid base64 encoding or decoding error.'}, status=400)
    
    if  mobile_number_pattern_validation(mobile_number):
        return mobile_number_pattern_validation(mobile_number)
    if ip_address in otp_requests_counter and otp_requests_counter[ip_address] != mobile_number and otp_requests_counter['counter']>MAX_COUNT_MOBILENO:
        return Response({'error': 'OTP request already sent for a different mobile number from this IP address.'}, status=429)
    

    otp, message = OTPService.request_otp(mobile_number)
    if not otp:
        return Response({'error': message}, status=429)
    
    otp_requests_counter[ip_address]=mobile_number
    otp_requests_counter['counter']+=1
    

    return Response({'otp': otp, 'message': message}, status=200)

@api_view(['POST'])
def verify_otp_view(request):
    serializer = VerifyOTPSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    mobile_number_base64 = serializer.validated_data['mobile_number_base64']
    user_otp = serializer.validated_data['user_otp']
    
    try:
        mobile_number = base64.b64decode(mobile_number_base64).decode('utf-8')
    except:
        return Response({'error': 'Invalid base64 encoding or decoding error.'}, status=400)

    if  mobile_number_pattern_validation(mobile_number):
        return mobile_number_pattern_validation(mobile_number)

    if otp_number_pattern_validation(user_otp):
        return otp_number_pattern_validation(user_otp)

    is_verified, message = OTPService.verify_otp(mobile_number, user_otp)
    if is_verified:
        return Response({'message': message}, status=200)
    else:
        return Response({'error': message}, status=400)
