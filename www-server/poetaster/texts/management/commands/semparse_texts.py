from texts.models import Text
from common.management.commands import BaseCommand
from nlp.backends.ccg2lambda import CCG2Lambda
from pprint import pprint


class Command(BaseCommand):

    def handle(self, *args, **options):
        ccg2lambda = CCG2Lambda()

        text = self.session.query(Text).first()

        doc = text.nlp_doc_versions[0]

        print(ccg2lambda.get_lambda_ccg(doc.generate()))
