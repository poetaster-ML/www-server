from django.apps import AppConfig


class TextsConfig(AppConfig):
    name = "texts"

    def ready(self):
        from poetaster.celery_app import app as celery_app
        from .tasks import (
            AnnotateTextTask,
            S3BucketImportTask,
            S3BucketPageImportTask,
        )
        for task in [
            AnnotateTextTask,
            S3BucketImportTask,
            S3BucketPageImportTask,
        ]:
            celery_app.tasks.register(task())
