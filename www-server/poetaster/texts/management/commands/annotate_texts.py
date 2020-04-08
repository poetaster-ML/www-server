from texts.models import Text
from common.management.commands import BaseCommand
from poetaster.celery_app import app as celery_app


class Command(BaseCommand):
    def handle(self, *args, **options):
        task = celery_app.tasks.get("texts.AnnotateTextsTask")

        for text in self.session.query(Text).all():
            _, pk, _ = self.session.identity_key(instance=text)
            task.apply_async(args=(pk,))
