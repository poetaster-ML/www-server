import graphene
from graphene import relay
from texts.models import Text

from ..common.fields import (
    FilterableConnectionField,
)

from .types import (
    TextConnection,
    SearchIndexedTextConnection,
    CollectionConnection
)

from .mutations import (
    UpdateText,
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

    def resolve_texts_search(root, info, query):
        return Text.search(query)


class TextsMutations(graphene.ObjectType):
    update_text = UpdateText.Field()
