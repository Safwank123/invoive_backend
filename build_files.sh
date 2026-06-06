#!/bin/bash

# Install Python dependencies (--break-system-packages needed for Vercel's managed env)
pip install -r requirements.txt --break-system-packages

# Collect static files for WhiteNoise to serve
python manage.py collectstatic --noinput
