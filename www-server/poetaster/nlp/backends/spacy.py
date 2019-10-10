import spacy
from .base import BaseBackend


class SpacyClient:
    def __init__(
        self, text,
        model="en_core_web_sm",
    ):
        self.nlp = spacy.load(model)
        self.doc = self.nlp(text)

    def get_tokens(self):
        return [token.text for token in self.doc]

    def get_parts_of_speech(self):
        return [token.pos for token in self.doc]

    def get_dependency_parse(self):
        return [(token.head.i, token.dep_) for token in self.doc]


class SpacyBackend(BaseBackend):
    def __init__(self, text):
        self.client = SpacyClient(text)

    def get_tokens(self):
        return self.client.get_tokens()

    def get_parts_of_speech(self):
        return self.client.get_parts_of_speech()

    def get_dependency_parse(self):
        return self.client.get_dependency_parse()
