import graphene
from graphene import (
    ObjectType, Mutation, Field, String, Int,
    AbstractType, ID, List, JSONString
)
from graphene_sqlalchemy import (
    SQLAlchemyObjectType, SQLAlchemyConnectionField as ConnectionField
)

from . import models

from core.schema import (
    VersionedObjectType, FilterableConnectionField, RelatedConnectionField
)


class CommonFields(AbstractType):
    pass


class CollectionField(SQLAlchemyObjectType, CommonFields):
    texts = List("texts.schema.TextField")

    class Meta:
        model = models.Collection
        interfaces = (graphene.Node,)


class TextToTextRelationField(SQLAlchemyObjectType, CommonFields):
    to_text = Field(lambda: TextField)
    commentary = String()

    class Meta:
        model = models.TextToTextRelation
        interfaces = (graphene.Node, )


class TextLabelField(SQLAlchemyObjectType, CommonFields):
    value = String()
    index = Int()

    class Meta:
        model = models.TextLabel


class TextLabelRelationField(SQLAlchemyObjectType, CommonFields):
    commentary = String()
    label = Field(TextLabelField)

    class Meta:
        model = models.TextLabelRelation
        interfaces = (graphene.Node,)


class NLPConstructCommonFields:
    value = JSONString()


class TextDependencyParseField(VersionedObjectType, NLPConstructCommonFields):
    class Meta:
        model = models.TextDependencyParse
        interfaces = (graphene.Node,)


class TextPartsOfSpeechField(VersionedObjectType, NLPConstructCommonFields):
    class Meta:
        model = models.TextPartsOfSpeech
        interfaces = (graphene.Node,)


class TextTokensField(VersionedObjectType, NLPConstructCommonFields):
    class Meta:
        model = models.TextTokens
        interfaces = (graphene.Node,)


class TextField(VersionedObjectType, CommonFields):
    collection = Field(CollectionField)
    author = Field("texts.schema.AuthorField")

    tokens_versions = RelatedConnectionField(TextTokensField)
    parts_of_speech_versions = RelatedConnectionField(TextPartsOfSpeechField)
    dependency_parse_versions = RelatedConnectionField(
        TextDependencyParseField)

    labels = ConnectionField(TextLabelRelationField)
    intertextual_relations = ConnectionField(TextToTextRelationField)

    class Meta:
        model = models.Text
        interfaces = (graphene.Node,)


class AuthorField(SQLAlchemyObjectType, CommonFields):
    name = String()
    texts = ConnectionField(TextField)
    collections = ConnectionField(CollectionField)

    class Meta:
        model = models.Author
        interfaces = (graphene.Node,)


class UpdateText(Mutation):
    class Arguments:
        id = ID()
        raw = String()

    person = Field(TextField)

    def mutate(self, info, id, raw):
        text = models.Text.query.get(id)
        text.raw = raw
        models.session.commit()
        return UpdateText(text=text)


class Query(ObjectType):
    texts = FilterableConnectionField(
        TextField,
        slug=String(),
        author_slug=String()
    )
    authors = FilterableConnectionField(AuthorField, slug=String())
    collections = ConnectionField(CollectionField)

    text_dependency_parses = FilterableConnectionField(
        TextDependencyParseField)


class Mutation(ObjectType):
    update_text = UpdateText.Field()
