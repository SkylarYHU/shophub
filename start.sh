#!/bin/bash

python manage.py migrate

python manage.py collectstatic --noinput

gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8080