from sqlalchemy import (
    Column, ForeignKey, Integer, String, Text, Date,
    ForeignKeyConstraint, PrimaryKeyConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import backref, relationship, scoped_session, sessionmaker
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy import create_engine

from sqlalchemy_utils import observes

from nlp import get_backend as get_nlp_backend

from common.models import (
    IDVersioned, SlugVersioned, relationship_ordered_by_version
)
from common.columns import SlugColumn
from common.utils.slug import slugify


Base = declarative_base()

engine = create_engine('postgresql://postgres@db:5432/postgres')

# Create database session object
session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
Base.query = session.query_property()


APP_TABLE_PREFIX = "texts"


class LocalFK(ForeignKey):
    default_column = "slug"

    def __init__(self, table, column=None, **kwargs):
        super().__init__(
            LocalFK.to_column(table, column or self.default_column),
            **kwargs
        )

    @classmethod
    def to_column(cls, table, column=None):
        return "%s_%s.%s" % (
            APP_TABLE_PREFIX, table, column or cls.default_column)


class Author(Base):
    __tablename__ = "texts_Author"

    name = Column(String)
    slug = SlugColumn(primary_key=True, source="name")

    birth_date = Column(Date, nullable=True)
    death_date = Column(Date, nullable=True)

    nationality = Column(String(255), nullable=True)

    collections = relationship("Collection", backref="author")
    texts = relationship("Text", backref="author")

    @observes("name")
    def generate_slug(self, name):
        self.slug = slugify(Author, name, session)

    @classmethod
    def search(cls, query):
        from .documents import AuthorDocument

        search = AuthorDocument.search()
        search = search.query(
          "multi_match", query=query, fields=["name"]
        )

        response = search.execute()

        return response


class Collection(Base):
    __tablename__ = "texts_Collection"

    title = Column(String(255))
    slug = SlugColumn(primary_key=True)

    author_slug = Column(String, LocalFK("Author"))

    texts = relationship("Text", backref="collection")


class NLPConstruct:
    value = Column(JSON)
    nlp_field = None

    @property
    def method(self):
        return "get_%s" % self.nlp_field

    def generate(self, *args, **kwargs):
        nlp_backend = get_nlp_backend()(self.text.raw)
        return getattr(nlp_backend, self.method)()


class TextVersionRelated:
    text_slug = Column(String)
    text_version = Column(Integer)

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                ["text_slug", "text_version"],
                [
                    LocalFK.to_column("Text"),
                    LocalFK.to_column("Text", "version")
                ]
            ),
        )


class VersionedTextVersionRelatedNLPConstruct(
    IDVersioned, TextVersionRelated, NLPConstruct
):
    @declared_attr
    def __table_args__(cls):
        return (
            IDVersioned.__table_args__ +
            TextVersionRelated.__table_args__
        )


class TextTokens(Base, VersionedTextVersionRelatedNLPConstruct):
    __tablename__ = "texts_TextTokens"
    nlp_field = "tokens"


class TextPartsOfSpeech(Base, VersionedTextVersionRelatedNLPConstruct):
    __tablename__ = "texts_TextPartsOfSpeech"
    nlp_field = "parts_of_speech"


class TextDependencyParse(Base, VersionedTextVersionRelatedNLPConstruct):
    __tablename__ = "texts_TextDependencyParse"
    nlp_field = "dependency_parse"


class TextNLPDoc(Base, VersionedTextVersionRelatedNLPConstruct):
    __tablename__ = "texts_TextNLPDoc"
    nlp_field = "doc"


class TextLabel(Base):
    __tablename__ = "texts_TextLabel"
    id = Column(Integer, primary_key=True)
    value = Column(String)


class TextLabelRelation(Base, IDVersioned):
    __tablename__ = "texts_TextLabelRelation"

    text_slug = Column(Integer)
    text_version = Column(Integer)

    label_id = Column(Integer, LocalFK("TextLabel", "id"))
    label = relationship("TextLabel", backref="text_relations")

    commentary = Column(String)
    text_index = Column(Integer)

    __table_args__ = (
        ForeignKeyConstraint(
            ["text_slug", "text_version"],
            [
                LocalFK.to_column("Text"),
                LocalFK.to_column("Text", "version")
            ]
        ),
        PrimaryKeyConstraint(
            "id", "version", "text_slug", "text_version", "label_id"
        ),
        UniqueConstraint("id", "version", name="text_label_version")
    )


class TextGenre(Base):
    __tablename__ = "texts_TextGenre"
    id = Column(Integer, primary_key=True)
    # text_id = Column(Integer, LocalFK("Text"))


class TextToTextRelation(Base, IDVersioned):
    __tablename__ = "texts_TextToTextRelation"

    from_text_slug = Column(String)
    from_text_version = Column(Integer)

    to_text_slug = Column(String)
    to_text_version = Column(Integer)

    commentary = Column(String, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["from_text_slug", "from_text_version"],
            [
                LocalFK.to_column("Text"),
                LocalFK.to_column("Text", "version")
            ], name="from_text"
        ),
        ForeignKeyConstraint(
            ["to_text_slug", "to_text_version"],
            [
                LocalFK.to_column("Text"),
                LocalFK.to_column("Text", "version")
            ], name="to_text"
        ),
        PrimaryKeyConstraint(
            "id", "version", "from_text_slug", "from_text_version",
            "to_text_slug",  "to_text_version"
        ),
        UniqueConstraint("id", "version", name="text_to_text_rel_version")
    )


class PoetryFoundationData(Base):
    __tablename__ = "texts_PoetryFoundationData"

    id = Column(Integer, primary_key=True)

    classification = Column(String)
    keywords = Column(ARRAY(String))
    period = Column(String)
    reference = Column(String)
    region = Column(String)

    text = relationship("Text", backref=backref(
        "poetry_foundation_data", uselist=False
    ))


class Text(Base, SlugVersioned):
    __tablename__ = "texts_Text"

    title = Column(String)
    year = Column(String, nullable=True)

    lines = Column(ARRAY(String))
    raw = Column(Text)

    author_slug = Column(String, LocalFK("Author"))

    collection_slug = Column(String, LocalFK("Collection"), nullable=True)

    poetry_foundation_data_id = Column(
        Integer, LocalFK("PoetryFoundationData", "id"), nullable=True
    )

    tokens_versions = relationship_ordered_by_version(
        TextTokens, backref="text")

    parts_of_speech_versions = relationship_ordered_by_version(
        TextPartsOfSpeech, backref="text")

    dependency_parse_versions = relationship_ordered_by_version(
        TextDependencyParse, backref="text")

    nlp_doc_versions = relationship_ordered_by_version(
        TextNLPDoc, backref="text")

    intertextual_relations = relationship(
        "Text",
        secondary="texts_TextToTextRelation",
        foreign_keys=(
            TextToTextRelation.from_text_slug,
            TextToTextRelation.from_text_version,
        ),
    )

    related_to = relationship(
        "Text",
        secondary="texts_TextToTextRelation",
        foreign_keys=(
            TextToTextRelation.to_text_slug,
            TextToTextRelation.to_text_version,
        ),
    )

    labels = relationship(
        "TextLabel",
        secondary="texts_TextLabelRelation",
        backref="texts"
    )

    @observes("title")
    def generate_slug(self, title):
        self.slug = slugify(Text, title, session)

    @classmethod
    def search(cls, query):
        from .documents import TextDocument

        search = TextDocument.search()
        search = search.query(
          "multi_match", query=query, fields=["title", "raw"]
        )

        search = search.highlight("title", fragment_size=0)
        search = search.highlight("raw", fragment_size=0)

        response = search.execute()

        return response

    def generate_nlp_constructs(self, session=session):
        for model, relation in [
            # (TextTokens, "tokens_versions",),
            # (TextPartsOfSpeech, "parts_of_speech_versions",),
            # (TextDependencyParse, "dependency_parse_versions",),
            (TextNLPDoc, "nlp_doc_versions")
        ]:
            collection = getattr(self, relation)

            if collection:
                # latest version
                instance = collection[0]
            else:
                instance = model(text=self)

            instance.value = instance.generate()
            session.add(instance)
