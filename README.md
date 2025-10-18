# AdmitionWala (Django)

This repository contains the Django-based AdmitionWala site used for college discovery and admissions.

Quick start (Windows / PowerShell):

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run migrations and start the dev server:

```powershell
python manage.py migrate
python manage.py runserver
```

3. Open http://127.0.0.1:8000/ in your browser.

Tests:

```powershell
python manage.py test
```

Notes & troubleshooting:
- If you see template errors about `{% static %}`, ensure templates load the static tag with `{% load static %}`.
- Per-page head content should override defaults using the `page_head` block in templates.

If you want, I can also add Docker/Gunicorn deployment steps and a production-ready static file setup.
