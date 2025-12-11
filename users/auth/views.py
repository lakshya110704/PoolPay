from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from users.models import OTP, User
from .serializers import SendOTPSerializer, VerifyOTPSerializer

# SimpleJWT imports
from rest_framework_simplejwt.tokens import RefreshToken

class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        # create_otp should exist (we created it earlier)
        from .send_otp import create_otp
        otp = create_otp(phone)
        # In prod: send via SMS provider. Here we echo for testing.
        return Response({"message": "OTP sent", "otp": otp.code}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        code = serializer.validated_data["code"]

        # Find latest matching OTP that is not used
        now = timezone.now()
        try:
            otp = OTP.objects.filter(phone=phone, is_used=False).order_by('-created_at').first()
            if not otp:
                return Response({"detail": "OTP not found"}, status=status.HTTP_400_BAD_REQUEST)
            if otp.code != code:
                otp.attempts += 1
                otp.save()
                return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            if otp.expires_at < now:
                return Response({"detail": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
        except OTP.DoesNotExist:
            return Response({"detail": "OTP not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Mark OTP used
        otp.is_used = True
        otp.save()

        # Get or create user by phone
        user, created = User.objects.get_or_create(phone=phone, defaults={"is_active": True})
        # Optionally set name/email later

        # Issue JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "access": access_token,
            "refresh": refresh_token,
            "user": {
                "id": str(user.id),
                "phone": user.phone,
                "name": user.name or ""
            }
        }, status=status.HTTP_200_OK)