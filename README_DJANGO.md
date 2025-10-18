# AditionWala (Django + SQLite demo)

This scaffold provides a small Django app with signup/login and simple AI-like endpoints backed by a small `nake_ml` module (pure Python). Uses SQLite so no DB setup is required.

Prerequisites
- Python 3.8+

Setup
1. Create and activate a venv:

   python -m venv venv
   .\venv\Scripts\Activate.ps1   # PowerShell

2. Install dependencies:

   pip install -r requirements.txt

3. Run migrations and start server:

   python manage.py migrate
   python manage.py runserver

4. Open http://127.0.0.1:8000/ in your browser.

API endpoints
- GET /api/health  — returns {"status":"ok"}
- POST /api/predict — accepts JSON: { interestLevel, budgetK, subscribed } and returns { score, hot }
- POST /api/recommend — returns { score, recommendations }

Notes
- This demo uses Django's auth system and SQLite. To switch to MySQL, update `DATABASES` in `aditionwala/settings.py` and install `mysqlclient`.
