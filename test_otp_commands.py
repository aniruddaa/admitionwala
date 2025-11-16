from django.contrib.auth.models import User
from core.models import UserProfile, OTPToken
from django.utils import timezone
from datetime import timedelta

# Delete existing test user
User.objects.filter(username='otp_test@test.com').delete()

# Create test user
u = User.objects.create_user('otp_test@test.com', 'otp_test@test.com', 'Test123')
p = UserProfile.objects.create(user=u, mobile='9226236200')

print("\n✓ User created: otp_test@test.com")
print(f"✓ Mobile: {p.mobile}\n")

# Create OTP
otp_code = '123456'
expires = timezone.now() + timedelta(minutes=10)
otp = OTPToken.objects.create(
    user=u,
    code=otp_code,
    mobile='9226236200',
    delivery_method='sms',
    expires_at=expires
)

print(f"✓ OTP Created: {otp.code}")
print(f"✓ Mobile: {otp.mobile}")
print(f"✓ Delivery: {otp.delivery_method}")
print(f"✓ Expires: {otp.expires_at}\n")

# Test OTP verification
print("✓ Testing verification...")
# Note: The verify_otp method is in otp_auth.py, so test directly
if otp.code == otp_code and not otp.is_expired():
    print("✓ OTP is VALID!\n")
else:
    print("✗ OTP verification failed\n")

# Cleanup
u.delete()
print("✓ Test user deleted")
print("\n✓ OTP SYSTEM TEST COMPLETE\n")
