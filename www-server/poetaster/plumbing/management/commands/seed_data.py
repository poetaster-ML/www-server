from texts.models import TextLabel
from common.management.commands import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for label_type in [
            "commentary",
        ]:

            instance = TextLabel(value=label_type)
            self.session.add(instance)
        self.session.commit()
