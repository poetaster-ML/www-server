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
        return [token.pos_ for token in self.doc]

    def get_dependency_parse(self):
        return [(token.head.i, token.dep_) for token in self.doc]

    def to_tree(self, tree, children):
        for token in children:
            node = self.token_data(token)
            tree.append(node)
        return tree

    def token_data(self, token):
        return {
            "text": token.text,
            "id": token.i,
            "start": token.idx,
            "end": token.idx + len(token),
            "pos": token.pos_,
            "tag": token.tag_,
            "dep": token.dep_,
            "head": token.head.i,
            "children": self.to_tree([], token.children)
        }

    def get_doc_by_sentence(self):
        for sent in self.doc.sents:
            tokens = [self.token_data(token) for token in sent]
            root = [
                token for token in tokens if token["head"] == token["id"]
            ][0]
            yield {
                "tokens": tokens,
                "tree": root
            }

    def get_doc(self):
        return list(self.get_doc_by_sentence())


class SpacyBackend(BaseBackend):
    def __init__(self, text):
        self.client = SpacyClient(text)

    def get_tokens(self):
        return self.client.get_tokens()

    def get_parts_of_speech(self):
        return self.client.get_parts_of_speech()

    def get_dependency_parse(self):
        return self.client.get_dependency_parse()

    def get_doc(self):
        return self.client.get_doc()
