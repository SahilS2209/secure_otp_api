from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import OTPService

@api_view(['POST'])
def request_otp_view(request):
    mobile_number = request.data.get('mobile_number')

    if not mobile_number.isdigit() or not (6 <= int(mobile_number[0]) <= 9) or len(mobile_number) != 10:
        return Response({'error': 'Please provide a valid 10-digit mobile number starting with a digit between 6 and 9.'}, status=400)

    otp, message = OTPService.request_otp(mobile_number)
    if not otp:
        return Response({'error': message}, status=429)

    return Response({'otp': otp, 'message': message}, status=200)

@api_view(['POST'])
def verify_otp_view(request):
    mobile_number = request.data.get('mobile_number')
    user_otp = request.data.get('otp')

    if not mobile_number.isdigit() or len(mobile_number) != 10:
        return Response({'error': 'Please provide a valid 10-digit mobile number.'}, status=400)

    if not user_otp.isdigit() or len(user_otp) != 6:
        return Response({'error': 'Please provide a valid 6-digit OTP.'}, status=400)

    is_verified, message = OTPService.verify_otp(mobile_number, user_otp)
    if is_verified:
        return Response({'message': message}, status=200)
    else:
        return Response({'error': message}, status=400)