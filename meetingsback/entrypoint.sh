#!/bin/sh

python manage.py migrate --no-input

mkdir -p /app/static
python manage.py collectstatic

gunicorn meetingsback.wsgi:application --bind 0.0.0.0:8000
#python manage.py runserver 0.0.0.0:8000