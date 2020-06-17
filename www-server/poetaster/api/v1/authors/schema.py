import graphene
from graphene import relay
from ..common.fields import (
    FilterableConnectionField,
)

from .types import (
    AuthorConnection,
    SearchIndexedAuthorConnection
)

from .mutations import (
  AuthorCreate
)

from texts.models import Author


class AuthorsQueries(graphene.ObjectType):
    authors = FilterableConnectionField(
        AuthorConnection,
        slug=graphene.String())

    authors_search = relay.ConnectionField(
        SearchIndexedAuthorConnection,
        query=graphene.String())

    def resolve_authors_search(root, info, query):
        return Author.search(query)


class AuthorsMutations(graphene.ObjectType):
    author_create = AuthorCreate.Field()
