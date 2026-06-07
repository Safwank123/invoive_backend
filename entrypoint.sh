#!/bin/sh
set -e

# Run migrations and collectstatic, then start Gunicorn
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn invoice_backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${GUNICORN_WORKERS:-3}
