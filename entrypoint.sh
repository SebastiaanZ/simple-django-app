#!/usr/bin/env bash

python manage.py waitforpostgres
python manage.py migrate --no-input
python manage.py collectstatic --no-input
gunicorn --bind=0.0.0.0:8080 simple_django_app.wsgi:application
