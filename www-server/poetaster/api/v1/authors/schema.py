import graphene

from ..common.fields import (
    FilterableConnectionField,
)

from .types import (
    AuthorConnection
)


class AuthorsQueries(graphene.ObjectType):
    authors = FilterableConnectionField(
        AuthorConnection,
        slug=graphene.String())
