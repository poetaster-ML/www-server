import graphene

import texts.schema


class Query(
    texts.schema.Query,
    graphene.ObjectType
):
    pass


class Mutation(
    texts.schema.Mutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
