import random
from datetime import timedelta
from django.utils import timezone
from users.models import OTP

def generate_otp():
    return str(random.randint(100000, 999999))

def create_otp(phone):
    code = generate_otp()
    now = timezone.now()

    otp = OTP.objects.create(
        phone=phone,
        code=code,
        expires_at=now + timedelta(minutes=5),
    )
    return otp