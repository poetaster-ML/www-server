from elasticsearch_dsl import Document, Text, Integer, Object, InnerDoc


class AuthorDocument(Document):
    name = Text()
    slug = Text()
    version = Integer()

    class Index:
        name = "authors"
        max_result_window = 10


class AuthorInnerDoc(InnerDoc):
    name = Text()
    slug = Text()


class TextDocument(Document):
    title = Text()
    raw = Text()
    slug = Text()
    version = Integer()
    author = Object(AuthorInnerDoc)

    class Index:
        name = "texts"
        max_result_window = 10
