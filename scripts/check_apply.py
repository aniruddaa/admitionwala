import os
import sys
# Ensure we're running from project base
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aditionwala.settings')
import django
django.setup()
from django.test import Client
c = Client()
for job_id in (1,2):
    path = f'/job/{job_id}/'
    print('--- GET', path)
    r = c.get(path)
    print('STATUS:', r.status_code)
    body = r.content.decode('utf-8', errors='replace')
    print(body[:8000])
    print('\n\n')
