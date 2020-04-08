from __future__ import absolute_import, unicode_literals
from .celery_app import app as celery_app

from elasticsearch_dsl import connections

connections.create_connection(
  hosts=['search:9200'],
  timeout=20
)

__all__ = ('celery_app',)
