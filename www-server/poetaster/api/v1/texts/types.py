import graphene
from graphene import relay

from texts import models
from ..common.types import (
    ModelObjectType,
    ModelNode,
    ModelNodeMeta,
    VersionedModelNode,
)

from ..common.fields import ConnectionField


class TextNLPDocNode(ModelNode):
    class Meta(ModelNodeMeta):
        model = models.TextNLPDoc


class TextLabelNode(ModelNode):
    class Meta(ModelNodeMeta):
        model = models.TextLabel


class TextLabelConnection(relay.Connection):
    class Meta:
        node = TextLabelNode

    class Edge:
        commentary = graphene.String()
        text_index = graphene.Int()


class TextLabelRelationNode(ModelNode):
    class Meta(ModelNodeMeta):
        model = models.TextLabelRelation


class IntertextualRelationNode(ModelNode):
    class Meta(ModelNodeMeta):
        model = models.TextToTextRelation


class TextNode(VersionedModelNode):
    nlp_doc_versions = ConnectionField(TextNLPDocNode.connection)
    labels = ConnectionField(TextLabelConnection)
    intertextual_relations = ConnectionField(IntertextualRelationNode.connection)

    class Meta(ModelNodeMeta):
        model = models.Text


class TextConnection(relay.Connection):
    class Meta:
        node = TextNode


class SearchIndexedTextNodeHighlights(graphene.ObjectType):
    title = graphene.String()
    raw = graphene.String()

    def resolve_title(self, info):
        if "title" in self:
            return self.title[0]

    def resolve_raw(self, info):
        if "raw" in self:
            return self.raw[0]


class SearchIndexedTextNode(graphene.ObjectType):
    slug = graphene.String()
    title = graphene.String()
    raw = graphene.String()
    version = graphene.Int()

    highlights = graphene.Field(SearchIndexedTextNodeHighlights)

    class Meta:
        interfaces = (relay.Node,)

    def resolve_highlights(self, info):
        return self.meta.highlight

    def resolve_id(self, info):
        return "%s.%s" % (self.slug, self.version)


class SearchIndexedTextConnection(relay.Connection):
    class Meta:
        node = SearchIndexedTextNode


class CollectionNode(ModelObjectType):
    class Meta(ModelNodeMeta):
        model = models.Collection


class CollectionConnection(relay.Connection):
    class Meta:
        node = CollectionNode
