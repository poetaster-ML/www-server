import graphene
from graphene import relay
from ..common.types import (
    ModelNode,
    ModelNodeMeta
)

from texts import models


class AuthorNode(ModelNode):
    class Meta(ModelNodeMeta):
        model = models.Author


class AuthorConnection(relay.Connection):
    class Meta:
        node = AuthorNode


class SearchIndexedAuthorNode(graphene.ObjectType):
    slug = graphene.String()
    name = graphene.String()

    class Meta:
        interfaces = (relay.Node,)


class SearchIndexedAuthorConnection(relay.Connection):
    class Meta:
        node = SearchIndexedAuthorNode
