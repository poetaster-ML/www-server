FROM python:3.7
RUN mkdir /app
WORKDIR /app

ENV PYTHONUNBUFFERED 1

ADD requirements.txt .
ADD poetaster poetaster
ADD gunicorn_config.py .
ADD manage.py .
ADD run.sh .
ADD wait-for.sh .

# local reqs
RUN pip install -r requirements.txt

# django reqs
ADD django-alchemy django-alchemy
RUN pip install -e django-alchemy

ENV PYTHONPATH $PYTHONPATH:/app:/app/poetaster
# ENV PYTHONPATH $PYTHONPATH:/app:/app/django-alchemy/django
ENV DJANGO_SETTINGS_MODULE poetaster.settings

RUN python -m spacy download en_core_web_sm
