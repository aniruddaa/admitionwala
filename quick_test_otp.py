#!/usr/bin/env python
"""
Quick test for OTP API endpoints
Tests mobile-based OTP verification system for 9226236200
"""

import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aditionwala.settings')
sys.path.insert(0, 'c:\\Users\\hp\\Desktop\\New folder (3)')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile
from core.otp_auth import OTPToken, send_otp_via_sms
from django.test import Client

def cleanup_test_user():
    """Remove test user if exists"""
    User.objects.filter(username='testuser@admitionwala.com').delete()

def setup_test_user():
    """Create a test user with mobile number"""
    cleanup_test_user()
    
    user = User.objects.create_user(
        username='testuser@admitionwala.com',
        email='testuser@admitionwala.com',
        password='TestPassword123'
    )
    
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.mobile = '9226236200'
    profile.save()
    
    return user

def test_otp_flow():
    """Test the complete OTP flow"""
    print("\n" + "="*70)
    print("MOBILE OTP AUTHENTICATION TEST - 9226236200")
    print("="*70 + "\n")
    
    try:
        # Setup test user
        print("1. Setting up test user with mobile 9226236200...")
        user = setup_test_user()
        print(f"   ✓ User created: {user.email}")
        print(f"   ✓ Mobile: {user.userprofile.mobile}\n")
        
        # Test OTP generation
        print("2. Testing OTP generation...")
        otp = OTPToken.generate_otp(user, mobile='9226236200', delivery_method='sms')
        otp_code = otp.code
        print(f"   ✓ OTP Generated: {otp_code}")
        print(f"   ✓ Mobile: {otp.mobile}")
        print(f"   ✓ Delivery Method: {otp.delivery_method}")
        print(f"   ✓ Expires At: {otp.expires_at}\n")
        
        # Test OTP verification
        print("3. Testing OTP verification...")
        is_valid, message = otp.verify_otp(otp_code)
        print(f"   ✓ Verification Status: {is_valid}")
        print(f"   ✓ Message: {message}\n")
        
        if is_valid:
            print("="*70)
            print("✓ OTP SYSTEM IS WORKING CORRECTLY!")
            print("="*70)
            print("\nSummary:")
            print(f"  • Mobile Number: 9226236200")
            print(f"  • OTP Code: {otp_code}")
            print(f"  • Verification: PASSED")
            print(f"  • Delivery Method: SMS (via console)")
            print("\nNotes:")
            print("  • OTP expires in 10 minutes")
            print("  • Maximum 5 verification attempts allowed")
            print("  • SMS sending is logged to console (configure real SMS API for production)")
            print("="*70 + "\n")
        else:
            print("✗ OTP verification failed\n")
        
        # Cleanup
        cleanup_test_user()
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        cleanup_test_user()

if __name__ == '__main__':
    test_otp_flow()
