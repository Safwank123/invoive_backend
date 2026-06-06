#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Collect static files for WhiteNoise to serve
python manage.py collectstatic --noinput
