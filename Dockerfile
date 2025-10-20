FROM python:3.11-slim

# Prevents Python from writing .pyc files to disk and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (cache layer)
COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

# Copy application source
COPY . /app

# Create directory for collected static files (if used)
RUN mkdir -p /vol/static

EXPOSE 8000

# Default command: run Gunicorn serving the Django WSGI app
CMD ["gunicorn", "aditionwala.wsgi:application", "-b", "0.0.0.0:8000", "--workers", "3"]
