#!/usr/bin/env python
manage.py shell

from django.contrib.auth.models import User
from core.models import UserProfile
from core.otp_auth import OTPToken

# Create test user
user = User.objects.create_user(username='otp_test@test.com', email='otp_test@test.com', password='Test123456')
profile = UserProfile.objects.create(user=user, mobile='9226236200')

# Generate OTP
otp = OTPToken.generate_otp(user, mobile='9226236200', delivery_method='sms')
print(f"OTP Code: {otp.code}")
print(f"Mobile: {otp.mobile}")

# Verify OTP
is_valid, msg = otp.verify_otp(otp.code)
print(f"Verification: {is_valid}")
print(f"Message: {msg}")

# Cleanup
user.delete()
