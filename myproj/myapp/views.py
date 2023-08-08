from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import OTPService
import base64
from .utils import validate_mobile_number


@api_view(['POST'])
def request_otp_view(request):
    encoded_mobile_number = request.data.get('mobile_number')

    if not encoded_mobile_number:
        return Response({'error': 'Please provide the encoded mobile number.'}, status=400)

    try:
        decoded_mobile_number = base64.b64decode(encoded_mobile_number).decode('utf-8')
    except:
        return Response({'error': 'Invalid encoded mobile number.'}, status=400)

    if not validate_mobile_number(decoded_mobile_number):
        return Response({'error': 'Please provide a valid 10-digit mobile number starting with a digit between 6 and 9.'}, status=400)

    otp, message = OTPService.request_otp(decoded_mobile_number)
    if not otp:
        return Response({'error': message}, status=429)

    return Response({'otp': otp, 'message': message}, status=200)

@api_view(['POST'])
def verify_otp_view(request):
    encoded_mobile_number = request.data.get('mobile_number')
    user_otp = request.data.get('otp')

    if not encoded_mobile_number:
        return Response({'error': 'Please provide the encoded mobile number.'}, status=400)

    try:
        decoded_mobile_number = base64.b64decode(encoded_mobile_number).decode('utf-8')
    except:
        return Response({'error': 'Invalid encoded mobile number.'}, status=400)

    if not validate_mobile_number(decoded_mobile_number):
        return Response({'error': 'Please provide a valid 10-digit mobile number starting with a digit between 6 and 9.'}, status=400)

    if not user_otp:
        return Response({'error': 'Please provide the OTP.'}, status=400)

    if len(str(user_otp)) != 6 or not str(user_otp).isdigit():
        return Response({'error': 'Please provide a valid 6-digit OTP.'}, status=400)

    is_verified, message = OTPService.verify_otp(decoded_mobile_number, user_otp)
    if is_verified:
        return Response({'message': message}, status=200)
    else:
        return Response({'error': message}, status=400)