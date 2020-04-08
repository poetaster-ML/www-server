import graphene
from texts import models


class UpdateText(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        raw = graphene.String()

    def mutate(self, info, id, raw):
        text = models.Text.query.get(id)
        text.raw = raw
        models.session.commit()
        return UpdateText(text=text)
