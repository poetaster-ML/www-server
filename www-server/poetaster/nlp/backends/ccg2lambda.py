import requests
from django.conf import settings
from .base import BaseBackend


class CCG2LambdaClient:
    def __init__(
        self,
    ):
        pass

    def get_lambda_ccg(self, doc):
        endpoint = "%s/%s" % (
            settings.NLP_CCG_2_LAMBDA_URL,
            "semparse"
        )
        requests.post(endpoint, json={"sentences": doc['sentences']})


class CCG2Lambda(BaseBackend):
    def __init__(self):
        self.client = CCG2LambdaClient()

    def get_lambda_ccg(self, doc):
        return self.client.get_lambda_ccg(doc)
