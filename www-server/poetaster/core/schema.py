from functools import partial
from inspect import signature
from graphql import ResolveInfo
from graphene.relay import Connection, Node
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.fields import (
    SQLAlchemyConnectionField
)


class VersionedObjectType(SQLAlchemyObjectType):
    def resolve_id(self, info):
        id, version = self.__mapper__.primary_key_from_instance(self)
        return "%s.%s" % (id, version)

    class Meta:
        abstract = True


class FilterableConnectionField(SQLAlchemyConnectionField):
    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query = super().get_query(model, info, sort)
        return query.filter_by(**args)


class RelatedConnectionField(SQLAlchemyConnectionField):
    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        from pprint import pprint
        pprint(info.root_value)
        pprint(info.context)
        return SQLAlchemyConnectionField.get_query(model, info, sort, **args)
