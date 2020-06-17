import graphene
from texts import models
from .types import TextNode, TextLabelRelationNode


class TextUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        raw = graphene.String()

    def mutate(self, info, id, raw):
        text = models.Text.query.get(id)
        text.raw = raw
        models.session.commit()
        return TextUpdate(text=text)


class TextCreate(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        author_slug = graphene.String()
        raw = graphene.String()
        lines = graphene.List(graphene.String)

    text = graphene.Field(TextNode)

    def mutate(cls, root, title, author_slug, raw, lines):
        text = models.Text(
          title=title, author_slug=author_slug, raw=raw, lines=lines)
        models.session.add(text)
        models.session.commit()
        return TextCreate(text=text)


class TextLabelRelationCreate(graphene.Mutation):
    class Arguments:
        text_slug = graphene.String()
        text_version = graphene.Int()

        label_id = graphene.Int()

        commentary = graphene.String()
        text_index = graphene.Int()

    text_label_relation = graphene.Field(TextLabelRelationNode)

    def mutate(
        cls,
        root,
        text_slug,
        text_version,
        label_id,
        commentary,
        text_index
    ):
        text_label_relation = models.TextLabelRelation(
          text_slug=text_slug,
          text_version=text_version,
          label_id=label_id,
          commentary=commentary,
          text_index=text_index
        )

        models.session.add(text_label_relation)
        models.session.commit()
        return TextLabelRelationCreate(text_label_relation=text_label_relation)
