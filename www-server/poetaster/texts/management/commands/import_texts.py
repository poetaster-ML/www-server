from common.management.commands import BaseCommand
from poetaster.celery_app import app as celery_app


class Command(BaseCommand):
    def handle(self, *args, **options):
        task = celery_app.tasks.get(
            "texts.S3BucketImportTask"
        )

        task.apply(kwargs={"annotate": True})
