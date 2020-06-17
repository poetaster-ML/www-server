import graphene
from texts import models
from .types import AuthorNode


class AuthorCreate(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    author = graphene.Field(AuthorNode)

    def mutate(cls, root, name):
        author = models.Author(name=name)
        models.session.add(author)
        models.session.commit()
        return AuthorCreate(author=author)
