#!/bin/bash

cd /app

django-admin migrate --noinput
django-admin collectstatic --noinput
gunicorn -c python:gunicorn_config --reload poetaster.wsgi:application