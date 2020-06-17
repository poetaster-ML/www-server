import graphene
from .authors.schema import (
    AuthorsQueries,
    AuthorsMutations
)
from .texts.schema import (
    TextsQueries,
    TextsMutations
)


class Query(
    AuthorsQueries,
    TextsQueries
):
    pass


class Mutation(
    AuthorsMutations,
    TextsMutations,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
