import os
import sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aditionwala.settings')
import django
django.setup()
from django.test import Client
c = Client()
path = '/media/college_logos/agriculture.jpeg'
r = c.get(path)
print('GET', path, 'STATUS:', r.status_code)
print('CONTENT-LEN:', len(r.content))
