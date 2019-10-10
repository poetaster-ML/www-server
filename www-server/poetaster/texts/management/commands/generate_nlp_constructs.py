from texts.models import Text
from core.management.commands import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for text in self.session.query(Text).all():
            text.generate_nlp_constructs(session=self.session)
            self.session.commit()
