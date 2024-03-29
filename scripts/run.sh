#!/bin/sh

# Enable exit on error
set -e

# Collect the applications static files.
python manage.py collectstatic --noinput

# Apply the migrations.
python manage.py migrate

# Start the Green Unicorn.
gunicorn -b :8000 --chdir /app repair_ninja.wsgi:application
