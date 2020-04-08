import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType


class ModelObjectType(SQLAlchemyObjectType):
    class Meta:
        abstract = True


class ModelNodeMeta:
    interfaces = (graphene.Node,)


class ModelNode(ModelObjectType):
    class Meta:
        abstract = True


class VersionedModelNode(ModelNode):
    def resolve_id(self, info):
        slug, version = self.__mapper__.primary_key_from_instance(self)
        return "%s.%s" % (slug, version)

    class Meta:
        abstract = True
