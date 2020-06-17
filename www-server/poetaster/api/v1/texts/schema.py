import graphene
from graphene import relay
from texts import models

from ..common.fields import (
    FilterableConnectionField,
)

from .types import (
    TextConnection,
    TextLabelConnection,
    SearchIndexedTextConnection,
    CollectionConnection
)

from .mutations import (
    TextUpdate,
    TextCreate,
)


class TextsQueries(graphene.ObjectType):
    texts = FilterableConnectionField(
        TextConnection,
        slug=graphene.String())

    texts_search = relay.ConnectionField(
        SearchIndexedTextConnection,
        query=graphene.String())

    collections = FilterableConnectionField(
        CollectionConnection,
        slug=graphene.String())

    text_labels = relay.ConnectionField(
        TextLabelConnection)

    def resolve_text_labels(root, info):
        return models.session.query(models.TextLabel).all()

    def resolve_texts_search(root, info, query):
        return models.Text.search(query)


class TextsMutations(graphene.ObjectType):
    # text_update = TextUpdate.Field()
    text_create = TextCreate.Field()
