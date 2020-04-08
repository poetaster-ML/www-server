from graphene.types.utils import get_type
from graphene_sqlalchemy.fields import (
    SQLAlchemyConnectionField
)


class ConnectionField(SQLAlchemyConnectionField):
    def __init__(self, type, *args, **kwargs):
        # SQLAlchemyConnectionField applies type checking to `type`
        # before a potential module string is resolved. Do that
        # first here.
        type = get_type(type)

        super().__init__(type, *args, **kwargs)


class SlugFilterableConnectionField(ConnectionField):
    @classmethod
    def get_query(cls, model, info, sort=None, slug=None, **kwargs):
        query = super().get_query(model, info, sort, **kwargs)
        if slug:
            query = query.filter_by(slug=slug)
        return query


class RelatedConnectionField(ConnectionField):
    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        return ConnectionField.get_query(model, info, sort, **args)


FilterableConnectionField = SlugFilterableConnectionField
