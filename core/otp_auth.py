# OTP Authentication Module
# Two-factor authentication via OTP (Email & SMS)
# SMS sending via HTTP API (for mobile numbers)

import random
import string
import requests
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import OTPToken


class OTPAuthenticationBackend:
    """Backend for OTP-based authentication"""

    def authenticate(self, request=None, email=None, otp_code=None):
        """Authenticate user using OTP"""
        if not email or not otp_code:
            return None
        
        try:
            user = User.objects.get(email=email)
            otp_token = OTPToken.objects.get(user=user)
            
            is_valid, message = otp_token.verify_otp(otp_code)
            
            if is_valid:
                return user
            return None
        except (User.DoesNotExist, OTPToken.DoesNotExist):
            return None

    def get_user(self, user_id):
        """Get user by ID"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def generate_otp_for_user(user, mobile=None, email=None):
    """Utility function to generate OTP for a user"""
    if not mobile and not email:
        return None, "Either mobile or email is required"
    
    delivery_method = 'sms' if mobile else 'email'
    otp = OTPToken.generate_otp(user, email=email, mobile=mobile, delivery_method=delivery_method)
    
    if mobile:
        return otp, f"OTP sent to {mobile}"
    return otp, f"OTP sent to {email}"


def verify_user_otp(user, otp_code):
    """Utility function to verify OTP for a user"""
    try:
        otp_token = OTPToken.objects.get(user=user)
        is_valid, message = otp_token.verify_otp(otp_code)
        return is_valid, message
    except OTPToken.DoesNotExist:
        return False, "OTP not found. Please request a new OTP."


def send_otp_via_sms(mobile, code):
    """Send OTP via SMS to mobile number"""
    try:
        from .sms_service import SMSService
        
        # Format mobile number
        formatted_mobile = mobile.replace('+', '').replace(' ', '')
        if formatted_mobile.startswith('91'):
            formatted_mobile = formatted_mobile[2:]
        
        # Create message
        message = f"Your AdmitionWala OTP is: {code}. Valid for 10 minutes. Do not share with anyone."
        
        # Send via configured SMS service
        result = SMSService.send(formatted_mobile, message, route='otp')
        
        if result['success']:
            print(f"✓ SMS sent to {mobile} | Request ID: {result.get('request_id')}")
            return True
        else:
            print(f"✗ SMS failed for {mobile}: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"✗ Error sending SMS: {str(e)}")
        return False


def send_otp_via_email(user, email, code):
    """Send OTP via Email"""
    try:
        subject = "Your AdmitionWala OTP Code"
        message = f"""
        Hello {user.first_name or user.username},
        
        Your One-Time Password (OTP) is: {code}
        
        This code expires in 10 minutes.
        Do not share this code with anyone.
        
        If you didn't request this code, please ignore this email.
        
        Best regards,
        AdmitionWala Team
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return False
