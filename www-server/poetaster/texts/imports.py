from sqlalchemy.inspection import inspect
from .models import (
    Text, Author, PoetryFoundationData,
)


# Poetry foundation data keys
# -------------------------------------------------------------------- #
AUTHOR = "author"
CLASSIF = "classification"
KEYWORDS = "keywords"
PERIOD = "period"
REFERENCE = "reference"
TEXT = "text"
TITLE = "title"
YEAR = "year"
REGION = "region"
# -------------------------------------------------------------------- #


class Import:
    model = None
    data_lookup_keys = []
    column_to_data_keys = {}

    def __init__(self, session, data, **kwargs):
        self.session = session
        data.update(kwargs)
        self.data = data

    @property
    def pk(self):
        return inspect(self.model).primary_key[0].name

    @property
    def columns(self):
        def get_val(k):
            if callable(k):
                return k(self)
            return self.data.get(k, None)

        return {
            k: get_val(v) for k, v in self.column_to_data_keys.items()
        }

    @property
    def lookup_vals(self):
        return {k: self.columns.get(k) for k in self.data_lookup_keys}

    def lookup(self):
        return self.session.query(self.model).filter_by(
            **self.lookup_vals).first()

    def process(self):
        instance = self.lookup()

        if instance:
            for k, v in self.columns.items():
                setattr(instance, k, v)
        else:
            instance = self.model(**self.columns)
            self.session.add(instance)
            self.session.commit()
            self.session.refresh(instance, [self.pk])

        return instance


class AuthorImport(Import):
    model = Author
    data_lookup_keys = ["name"]
    column_to_data_keys = {
        "name": AUTHOR
    }


class PoetryFoundationDataImport(Import):
    model = PoetryFoundationData
    data_lookup_keys = ["text"]
    column_to_data_keys = {
        CLASSIF: CLASSIF,
        KEYWORDS: KEYWORDS,
        PERIOD: PERIOD,
        REFERENCE: REFERENCE,
        REGION: REGION
    }

    def lookup(self):
        return self.session.query(self.model) \
            .filter(self.model.text.contains(self.data["text"])) \
            .first()


class TextImport(Import):
    model = Text
    data_lookup_keys = ["title", "author_slug"]
    column_to_data_keys = {
        "author_slug": "author_slug",
        "lines": TEXT,
        "raw": lambda self: "\n".join(self.data.get(TEXT)),
        YEAR: YEAR,
        TITLE: TITLE
    }
