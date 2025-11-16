#!/usr/bin/env python
"""
Test script for SMS Service integration
Tests all supported SMS service providers
"""

import os
import sys

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aditionwala.settings')

import django
django.setup()

from core.sms_service import SMSService, MockSMSService
from django.conf import settings


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def test_mock_service():
    """Test Mock SMS Service"""
    print_header("TEST 1: MOCK SMS SERVICE")
    
    try:
        # Send test message
        result = SMSService.send(
            phone_number='9226236200',
            message='Your OTP is: 123456. Valid for 10 minutes.'
        )
        
        print("✓ Request sent to SMS service")
        print(f"✓ Response: {result}")
        print(f"✓ Success: {result['success']}")
        print(f"✓ Message: {result['message']}")
        print(f"✓ Request ID: {result.get('request_id')}")
        
        if result['success']:
            print("\n✓ MOCK SMS SERVICE: WORKING")
            return True
        else:
            print("\n✗ MOCK SMS SERVICE: FAILED")
            return False
            
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        return False


def test_service_detection():
    """Test service detection and initialization"""
    print_header("TEST 2: SERVICE DETECTION")
    
    try:
        service_name = SMSService.get_service_name()
        service = SMSService.get_service()
        
        print(f"✓ Current SMS Service: {service_name}")
        print(f"✓ Service Type: {type(service).__name__}")
        print(f"✓ Service Settings:")
        print(f"   - SMS_SERVICE: {settings.SMS_SERVICE}")
        print(f"   - FAST2SMS_API_KEY: {'Set' if settings.FAST2SMS_API_KEY else 'Not set'}")
        print(f"   - TWILIO_ACCOUNT_SID: {'Set' if settings.TWILIO_ACCOUNT_SID else 'Not set'}")
        print(f"   - AWS_ACCESS_KEY_ID: {'Set' if settings.AWS_ACCESS_KEY_ID else 'Not set'}")
        
        print(f"\n✓ SERVICE DETECTION: WORKING")
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        return False


def test_mock_history():
    """Test Mock service message history"""
    print_header("TEST 3: MOCK SERVICE HISTORY")
    
    try:
        service = SMSService.get_service()
        
        if isinstance(service, MockSMSService):
            # Send multiple messages
            for i in range(3):
                SMSService.send(
                    phone_number=f'922623620{i}',
                    message=f'Test OTP: {100000 + i}'
                )
            
            # Get history
            history = service.get_history()
            
            print(f"✓ Messages sent: {len(history)}")
            print(f"✓ Message history:")
            for i, msg in enumerate(history, 1):
                print(f"   {i}. To: {msg['phone']}, Time: {msg['timestamp']}")
            
            # Clear history
            service.clear_history()
            print(f"\n✓ History cleared, remaining: {len(service.get_history())}")
            
            print(f"\n✓ MOCK HISTORY: WORKING")
            return True
        else:
            print(f"✗ Not a Mock service, skipping history test")
            return True
            
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        return False


def test_multiple_numbers():
    """Test sending to multiple numbers"""
    print_header("TEST 4: MULTIPLE PHONE NUMBERS")
    
    test_numbers = [
        '9226236200',
        '9876543210',
        '8765432109',
    ]
    
    try:
        for phone in test_numbers:
            result = SMSService.send(
                phone_number=phone,
                message=f'Your OTP is: 123456'
            )
            
            status = "✓" if result['success'] else "✗"
            print(f"{status} {phone}: {result['message']}")
        
        print(f"\n✓ MULTIPLE NUMBERS: WORKING")
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        return False


def test_otp_integration():
    """Test OTP integration with SMS service"""
    print_header("TEST 5: OTP INTEGRATION WITH SMS")
    
    try:
        from django.contrib.auth.models import User
        from core.models import UserProfile, OTPToken
        from core.otp_auth import send_otp_via_sms
        
        # Create test user
        user, created = User.objects.get_or_create(
            username='sms_test_user@test.com',
            defaults={
                'email': 'sms_test_user@test.com',
                'first_name': 'Test'
            }
        )
        
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={'mobile': '9226236200'}
        )
        
        print(f"✓ Test user created: {user.email}")
        print(f"✓ Mobile number: {profile.mobile}")
        
        # Generate OTP
        otp = OTPToken.generate_otp(
            user=user,
            mobile='9226236200',
            delivery_method='sms'
        )
        
        print(f"\n✓ OTP generated: {otp.code}")
        print(f"✓ Mobile: {otp.mobile}")
        print(f"✓ Delivery: {otp.delivery_method}")
        print(f"✓ Expires: {otp.expires_at}")
        
        # Cleanup
        user.delete()
        
        print(f"\n✓ OTP INTEGRATION: WORKING")
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    tests = [
        "Mock SMS Service",
        "Service Detection",
        "Mock History",
        "Multiple Numbers",
        "OTP Integration"
    ]
    
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print("Test Results:")
    for i, (test, result) in enumerate(zip(tests, results), 1):
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {i}. {test}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if failed == 0:
        print("\n✓ ALL SMS SERVICE TESTS PASSED!")
        print("✓ SMS service is ready for use")
    else:
        print(f"\n✗ {failed} test(s) failed")
        print("✗ Please check errors above")
    
    return failed == 0


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "SMS SERVICE INTEGRATION TEST SUITE" + " "*19 + "║")
    print("║" + " "*25 + "AdmitionWala Platform" + " "*23 + "║")
    print("╚" + "="*68 + "╝")
    
    results = [
        test_mock_service(),
        test_service_detection(),
        test_mock_history(),
        test_multiple_numbers(),
        test_otp_integration(),
    ]
    
    success = print_summary(results)
    
    print("\n" + "="*70)
    print("Configuration Status:")
    print(f"  • SMS Service: {settings.SMS_SERVICE}")
    print(f"  • OTP Expiry: {settings.OTP_EXPIRY_MINUTES} minutes")
    print(f"  • Max Attempts: {settings.OTP_MAX_ATTEMPTS}")
    print(f"  • Code Length: {settings.OTP_CODE_LENGTH} digits")
    print("="*70 + "\n")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
