#!/bin/sh
set -e

# Run migrations only if DATABASE_URL is set
if [ -n "$DATABASE_URL" ]; then
  python manage.py migrate --noinput
fi

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn invoice_backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${GUNICORN_WORKERS:-3}
