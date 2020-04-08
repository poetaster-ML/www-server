#!/bin/bash

COMMAND="$1"
shift
case "$COMMAND" in

    dj)
        django-admin $@
        ;;

    dev)
        cd /app

        django-admin migrate --noinput
        django-admin collectstatic --noinput
        gunicorn -c python:gunicorn_config --reload poetaster.wsgi:application
        ;;

    worker)
        celery -A poetaster.celery_app worker -l INFO -P gevent -c 5 $@
        ;;

    flower)
        celery -A poetaster.celery_app flower --address=0.0.0.0 --port=8669 -l info
        ;;

    *)
        echo "Unrecognized command: $COMMAND"
        exit 1

esac
