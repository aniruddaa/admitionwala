# SMS Service Module
# Supports: Fast2SMS (India), Twilio (Global), AWS SNS, Mock (Testing)

import requests
import json
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class SMSServiceException(Exception):
    """Custom exception for SMS service errors"""
    pass


class Fast2SMSService:
    """Fast2SMS Service - India's free SMS API (https://www.fast2sms.com/)"""
    
    def __init__(self, api_key):
        """
        Initialize Fast2SMS service
        
        Args:
            api_key (str): Your Fast2SMS API key from https://www.fast2sms.com/
        """
        self.api_key = api_key
        self.url = "https://www.fast2sms.com/dev/bulkV2"
        
    def send(self, phone_number, message, route='otp'):
        """
        Send SMS via Fast2SMS
        
        Args:
            phone_number (str): 10-digit mobile number without country code
            message (str): SMS message text
            route (str): SMS route type (otp, transactional, etc.)
            
        Returns:
            dict: {'success': bool, 'request_id': str, 'message': str}
        """
        try:
            # Format phone number
            phone = phone_number.replace('+', '').replace(' ', '')
            if not phone.startswith('91'):
                phone = '91' + phone
            
            params = {
                'authorization': self.api_key,
                'variables_values': message.split(':')[1].strip() if ':' in message else message,
                'route': route,
                'numbers': phone_number,  # Send without country code
            }
            
            response = requests.get(self.url, params=params, timeout=10)
            result = response.json()
            
            if result.get('return'):
                return {
                    'success': True,
                    'request_id': result.get('request_id'),
                    'message': f'SMS sent successfully to {phone_number}',
                    'raw_response': result
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', 'Failed to send SMS'),
                    'raw_response': result
                }
                
        except requests.exceptions.Timeout:
            raise SMSServiceException('Fast2SMS API request timed out')
        except requests.exceptions.RequestException as e:
            raise SMSServiceException(f'Fast2SMS API error: {str(e)}')
        except json.JSONDecodeError:
            raise SMSServiceException('Invalid response from Fast2SMS API')


class TwilioService:
    """Twilio Service - Global SMS (https://www.twilio.com/)"""
    
    def __init__(self, account_sid, auth_token, from_number):
        """
        Initialize Twilio service
        
        Args:
            account_sid (str): Twilio Account SID
            auth_token (str): Twilio Auth Token
            from_number (str): Twilio phone number (with country code)
        """
        try:
            from twilio.rest import Client
            self.client = Client(account_sid, auth_token)
            self.from_number = from_number
        except ImportError:
            raise SMSServiceException('twilio-python is not installed. Run: pip install twilio')
    
    def send(self, phone_number, message):
        """
        Send SMS via Twilio
        
        Args:
            phone_number (str): 10-digit mobile number
            message (str): SMS message text
            
        Returns:
            dict: {'success': bool, 'request_id': str, 'message': str}
        """
        try:
            # Format phone number with country code
            phone = f"+91{phone_number.replace('+', '').replace(' ', '')}"
            
            msg = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=phone
            )
            
            return {
                'success': True,
                'request_id': msg.sid,
                'message': f'SMS sent successfully to {phone_number}',
                'raw_response': {'sid': msg.sid, 'status': msg.status}
            }
            
        except Exception as e:
            raise SMSServiceException(f'Twilio API error: {str(e)}')


class AWSSNSService:
    """AWS SNS Service - Global SMS (https://aws.amazon.com/sns/)"""
    
    def __init__(self, access_key_id, secret_access_key, region_name='us-east-1'):
        """
        Initialize AWS SNS service
        
        Args:
            access_key_id (str): AWS Access Key ID
            secret_access_key (str): AWS Secret Access Key
            region_name (str): AWS Region
        """
        try:
            import boto3
            self.sns = boto3.client(
                'sns',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region_name
            )
        except ImportError:
            raise SMSServiceException('boto3 is not installed. Run: pip install boto3')
    
    def send(self, phone_number, message):
        """
        Send SMS via AWS SNS
        
        Args:
            phone_number (str): 10-digit mobile number
            message (str): SMS message text
            
        Returns:
            dict: {'success': bool, 'request_id': str, 'message': str}
        """
        try:
            # Format phone number with country code
            phone = f"+91{phone_number.replace('+', '').replace(' ', '')}"
            
            response = self.sns.publish(
                PhoneNumber=phone,
                Message=message,
                MessageAttributes={
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': 'AdmitionWala'
                    },
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )
            
            return {
                'success': True,
                'request_id': response['MessageId'],
                'message': f'SMS sent successfully to {phone_number}',
                'raw_response': response
            }
            
        except Exception as e:
            raise SMSServiceException(f'AWS SNS error: {str(e)}')


class MockSMSService:
    """Mock SMS Service for Testing"""
    
    def __init__(self):
        """Initialize Mock service"""
        self.messages = []
    
    def send(self, phone_number, message, **kwargs):
        """
        Mock SMS sending (logs to console for testing)
        
        Args:
            phone_number (str): Mobile number
            message (str): SMS message
            **kwargs: Additional parameters (route, etc.) - ignored for mock
            
        Returns:
            dict: {'success': bool, 'request_id': str, 'message': str}
        """
        self.messages.append({
            'phone': phone_number,
            'message': message,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        })
        
        print(f"\n[MOCK SMS] To: {phone_number}")
        print(f"[MOCK SMS] Message: {message}\n")
        
        return {
            'success': True,
            'request_id': f'mock-{len(self.messages)}',
            'message': f'SMS sent successfully to {phone_number}',
            'raw_response': {'mock': True}
        }
    
    def get_history(self):
        """Get all sent messages (for testing)"""
        return self.messages
    
    def clear_history(self):
        """Clear message history"""
        self.messages = []


class SMSService:
    """Main SMS Service Manager - Handles multiple providers"""
    
    _instance = None
    _service = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one SMS service instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_service()
        return cls._instance
    
    @classmethod
    def _initialize_service(cls):
        """Initialize the appropriate SMS service based on settings"""
        service_type = getattr(settings, 'SMS_SERVICE', 'mock').lower()
        
        if service_type == 'fast2sms':
            api_key = getattr(settings, 'FAST2SMS_API_KEY', None)
            if not api_key:
                raise ImproperlyConfigured(
                    'FAST2SMS_API_KEY not set in Django settings'
                )
            cls._service = Fast2SMSService(api_key)
            print("✓ Fast2SMS service initialized")
            
        elif service_type == 'twilio':
            account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
            auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
            from_number = getattr(settings, 'TWILIO_FROM_NUMBER', None)
            
            if not all([account_sid, auth_token, from_number]):
                raise ImproperlyConfigured(
                    'Twilio credentials not set in Django settings'
                )
            cls._service = TwilioService(account_sid, auth_token, from_number)
            print("✓ Twilio service initialized")
            
        elif service_type == 'aws_sns':
            access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
            secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
            region = getattr(settings, 'AWS_SNS_REGION', 'us-east-1')
            
            if not all([access_key, secret_key]):
                raise ImproperlyConfigured(
                    'AWS credentials not set in Django settings'
                )
            cls._service = AWSSNSService(access_key, secret_key, region)
            print("✓ AWS SNS service initialized")
            
        elif service_type == 'mock':
            cls._service = MockSMSService()
            print("✓ Mock SMS service initialized (for testing)")
            
        else:
            raise ImproperlyConfigured(
                f'Unknown SMS_SERVICE: {service_type}. '
                'Supported: fast2sms, twilio, aws_sns, mock'
            )
    
    @staticmethod
    def send(phone_number, message, **kwargs):
        """
        Send SMS message
        
        Args:
            phone_number (str): 10-digit mobile number
            message (str): SMS text message
            
        Returns:
            dict: {'success': bool, 'request_id': str, 'message': str}
        """
        service = SMSService()
        return service._service.send(phone_number, message, **kwargs)
    
    @staticmethod
    def get_service():
        """Get current service instance"""
        service = SMSService()
        return service._service
    
    @staticmethod
    def get_service_name():
        """Get name of current service"""
        service = SMSService()
        if isinstance(service._service, Fast2SMSService):
            return 'Fast2SMS'
        elif isinstance(service._service, TwilioService):
            return 'Twilio'
        elif isinstance(service._service, AWSSNSService):
            return 'AWS SNS'
        elif isinstance(service._service, MockSMSService):
            return 'Mock (Testing)'
        return 'Unknown'
