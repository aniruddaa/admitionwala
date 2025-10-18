import os
import sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aditionwala.settings')
import django
django.setup()
from django.test import Client
from core.models import College

print('Colleges:')
for c in College.objects.all()[:20]:
    print(c.id, '-', c.name, 'logo=', bool(c.logo), 'bg=', bool(c.background_image))

# pick first college if exists
if College.objects.exists():
    col = College.objects.first()
    client = Client()
    path = f'/college/{col.id}/'
    print('\nFetching', path)
    r = client.get(path)
    print('STATUS:', r.status_code)
    print(r.content.decode('utf-8', errors='replace')[:10000])
else:
    print('No colleges in DB')
