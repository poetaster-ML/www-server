from django.conf import settings
from graphene_django.views import GraphQLView

from .schema import schema


class APIView(GraphQLView):
    schema = schema
    graphiql = settings.DEBUG
