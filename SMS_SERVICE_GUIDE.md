# SMS Service Configuration Guide

## Overview
The AdmitionWala platform now supports multiple SMS services for OTP delivery. You can choose the service that best fits your needs.

## Supported SMS Services

### 1. **Fast2SMS** (RECOMMENDED FOR INDIA) ⭐
- **Website:** https://www.fast2sms.com/
- **Cost:** Free 100 SMS/month (trial), then ~₹0.50/SMS
- **Coverage:** India
- **Setup Time:** 5 minutes
- **Best For:** Indian users, cost-conscious, rapid deployment

#### Features:
✓ No credit card required initially
✓ Instant OTP delivery
✓ Free trial tier
✓ Simple API
✓ India-optimized

#### Setup Steps:

1. **Sign Up**
   - Go to https://www.fast2sms.com/
   - Click "Sign Up"
   - Enter email and phone number
   - Verify email and phone

2. **Get API Key**
   - Log in to your dashboard
   - Go to Account Settings → API Key
   - Copy your API key (looks like: `xxxxx-xxxxx-xxxxx`)

3. **Configure Django**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env and add:
   SMS_SERVICE=fast2sms
   FAST2SMS_API_KEY=your_api_key_here
   ```

4. **Test**
   ```bash
   python manage.py shell
   from core.sms_service import SMSService
   result = SMSService.send('9226236200', 'Test OTP: 123456')
   print(result)
   # Should show: {'success': True, ...}
   ```

---

### 2. **Twilio** (GLOBAL)
- **Website:** https://www.twilio.com/
- **Cost:** Free $15 trial, then $0.0075/SMS
- **Coverage:** 1000+ countries
- **Setup Time:** 10 minutes
- **Best For:** Global coverage, enterprise use

#### Features:
✓ Global coverage
✓ Reliable, enterprise-grade
✓ Also supports voice calls
✓ Rich API
✓ Good documentation

#### Setup Steps:

1. **Sign Up**
   - Go to https://www.twilio.com/
   - Click "Sign Up Free"
   - Verify email and phone
   - Complete identity verification

2. **Get Credentials**
   - Go to https://console.twilio.com/
   - Copy: Account SID, Auth Token
   - Buy or verify a phone number
   - Note: Your Twilio phone number (e.g., +1234567890)

3. **Configure Django**
   ```bash
   # Edit .env and add:
   SMS_SERVICE=twilio
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_FROM_NUMBER=+1234567890
   ```

4. **Test**
   ```bash
   pip install twilio
   python manage.py shell
   from core.sms_service import SMSService
   result = SMSService.send('9226236200', 'Test OTP: 123456')
   print(result)
   ```

---

### 3. **AWS SNS** (GLOBAL)
- **Website:** https://aws.amazon.com/sns/
- **Cost:** Pay-as-you-go (~$0.075/SMS), free tier available
- **Coverage:** 200+ countries
- **Setup Time:** 15 minutes
- **Best For:** AWS users, large scale, enterprise

#### Features:
✓ AWS ecosystem integration
✓ Highly scalable
✓ Free tier SMS credits
✓ Rich monitoring
✓ Enterprise SLA

#### Setup Steps:

1. **Create AWS Account**
   - Go to https://aws.amazon.com/
   - Sign up with email and payment method

2. **Create IAM User**
   - Go to IAM Console
   - Create new user with SNS full access
   - Generate Access Key and Secret Key

3. **Configure Django**
   ```bash
   # Edit .env and add:
   SMS_SERVICE=aws_sns
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_SNS_REGION=us-east-1
   ```

4. **Test**
   ```bash
   pip install boto3
   python manage.py shell
   from core.sms_service import SMSService
   result = SMSService.send('9226236200', 'Test OTP: 123456')
   print(result)
   ```

---

### 4. **Mock** (TESTING ONLY)
- **Website:** Built-in
- **Cost:** Free
- **Coverage:** N/A (logs to console)
- **Setup Time:** 0 minutes
- **Best For:** Development and testing

#### Features:
✓ No API key needed
✓ SMS logged to console
✓ Perfect for testing
✓ No external API calls

#### Setup:
```bash
# Default, no setup needed
SMS_SERVICE=mock
```

#### Usage:
```bash
python manage.py shell
from core.sms_service import SMSService

# Send test SMS
result = SMSService.send('9226236200', 'Test OTP: 123456')

# Check mock history
service = SMSService.get_service()
if hasattr(service, 'messages'):
    print(service.messages)
```

---

## Quick Start (Recommended: Fast2SMS)

### 1. Sign up at Fast2SMS
```bash
# Go to https://www.fast2sms.com/
# Sign up → Verify → Get API key
```

### 2. Create .env file
```bash
cd /path/to/admitionwala
cp .env.example .env
```

### 3. Edit .env
```bash
# .env
SMS_SERVICE=fast2sms
FAST2SMS_API_KEY=paste_your_api_key_here
```

### 4. Test SMS
```bash
python manage.py shell
```

```python
from core.sms_service import SMSService

# Test sending OTP
result = SMSService.send('9226236200', 'Your OTP is: 123456')

# Check result
print(result)
# Output: {'success': True, 'request_id': '...', 'message': 'SMS sent...'}
```

### 5. Remove OTP from API response (Production)
In `core/views.py`, remove the `otp` field from responses:

```python
# Before (development)
return JsonResponse({
    'success': True,
    'otp': otp.code  # REMOVE THIS LINE
})

# After (production)
return JsonResponse({
    'success': True,
    'message': f'OTP sent to {mobile}'
})
```

---

## Environment Variable Setup

### Local Development (.env file)
```bash
# Create .env in project root
SMS_SERVICE=fast2sms
FAST2SMS_API_KEY=your_api_key

# Load in Python
from django.conf import settings
print(settings.SMS_SERVICE)
```

### Heroku Deployment
```bash
# Set environment variables
heroku config:set SMS_SERVICE=fast2sms
heroku config:set FAST2SMS_API_KEY=your_api_key

# Verify
heroku config
```

### AWS Deployment
```bash
# Use Systems Manager Parameter Store
aws ssm put-parameter --name SMS_SERVICE --value fast2sms
aws ssm put-parameter --name FAST2SMS_API_KEY --value your_api_key

# Or use Lambda environment variables
```

### Docker Deployment
```yaml
# docker-compose.yml
version: '3'
services:
  web:
    image: admitionwala:latest
    environment:
      SMS_SERVICE: fast2sms
      FAST2SMS_API_KEY: ${FAST2SMS_API_KEY}
```

### Kubernetes Deployment
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: sms-config
data:
  SMS_SERVICE: fast2sms

---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: sms-credentials
type: Opaque
data:
  FAST2SMS_API_KEY: <base64-encoded-key>
```

---

## Troubleshooting

### Issue: "FAST2SMS_API_KEY not set in Django settings"
**Solution:**
```bash
# Check .env file exists
cat .env

# Verify SMS_SERVICE is set
export SMS_SERVICE=fast2sms
export FAST2SMS_API_KEY=your_key

# Test settings
python manage.py shell
from django.conf import settings
print(settings.FAST2SMS_API_KEY)
```

### Issue: SMS not being sent
**Solution:**
```bash
# Enable debug mode
python manage.py shell
from core.sms_service import SMSService
result = SMSService.send('9226236200', 'Test')
print(result)  # Check for error details

# Check service status
print(SMSService.get_service_name())
```

### Issue: "twilio-python is not installed"
**Solution:**
```bash
pip install twilio
```

### Issue: "boto3 is not installed"
**Solution:**
```bash
pip install boto3
```

### Issue: Fast2SMS returning error
**Reasons:**
- Invalid API key
- Wrong mobile number format (should be 10 digits)
- Rate limit exceeded (max 1 SMS/second)
- Account suspended or out of quota

**Check:**
```bash
# Verify API key is correct
echo $FAST2SMS_API_KEY

# Verify mobile format (should be 10 digits)
mobile = '9226236200'  # ✓ Correct
mobile = '+919226236200'  # ✗ Wrong (has country code)

# Test with mock service first
SMS_SERVICE=mock python manage.py shell
```

---

## Production Checklist

- [ ] Choose SMS service (Fast2SMS recommended)
- [ ] Get API credentials
- [ ] Create .env file with credentials
- [ ] Add .env to .gitignore
- [ ] Test SMS sending
- [ ] Remove OTP from API responses
- [ ] Set DEBUG = False
- [ ] Configure HTTPS
- [ ] Set up monitoring/alerts
- [ ] Test end-to-end OTP flow
- [ ] Document for team
- [ ] Set up backups
- [ ] Monitor SMS quota/billing
- [ ] Test error handling

---

## Cost Comparison

| Service | Setup | Trial | Price | Best For |
|---------|-------|-------|-------|----------|
| **Fast2SMS** | 5 min | 100 SMS free | ₹0.50/SMS | India, startups |
| **Twilio** | 10 min | $15 free | $0.0075/SMS | Global, enterprise |
| **AWS SNS** | 15 min | $1 free | ~$0.075/SMS | AWS users, scale |
| **Mock** | 0 min | N/A | Free | Testing only |

---

## Code Examples

### Python - Direct SMS Sending
```python
from core.sms_service import SMSService

# Send OTP
result = SMSService.send(
    phone_number='9226236200',
    message='Your OTP is: 123456. Valid for 10 minutes.'
)

if result['success']:
    print(f"SMS sent! Request ID: {result['request_id']}")
else:
    print(f"Error: {result['message']}")
```

### Django ORM - OTP Generation
```python
from core.models import OTPToken
from django.contrib.auth.models import User

user = User.objects.get(email='user@example.com')

# Generate and send OTP
otp = OTPToken.generate_otp(
    user=user,
    mobile='9226236200',
    delivery_method='sms'
)

print(f"OTP created: {otp.code}")
```

### API Integration
```python
# In core/views.py
from core.sms_service import SMSService

def api_send_otp(request):
    mobile = request.POST.get('mobile')
    
    # Generate OTP...
    otp = OTPToken.generate_otp(user, mobile=mobile, delivery_method='sms')
    
    # SMSService.send() is called automatically in generate_otp()
    # via send_otp_via_sms() function
    
    return JsonResponse({'success': True})
```

---

## Resources

- **Fast2SMS Docs:** https://www.fast2sms.com/dev/api-docs/
- **Twilio Docs:** https://www.twilio.com/docs/sms
- **AWS SNS Docs:** https://docs.aws.amazon.com/sns/
- **Django Security:** https://docs.djangoproject.com/en/stable/topics/security/

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review service provider documentation
3. Check Django logs
4. Contact support of your chosen SMS service

---

**Status:** ✓ SMS Service Configuration Complete  
**Version:** 2.0  
**Last Updated:** November 16, 2025
