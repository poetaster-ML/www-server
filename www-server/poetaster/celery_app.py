from __future__ import absolute_import, unicode_literals

from celery import Celery

from django.conf import settings # noqa

app = Celery('poetaster', backend=None)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
