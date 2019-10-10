from django.http import HttpResponse
from django.middleware import csrf
from graphene_django.views import GraphQLView as _GraphQLView

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def serve_csrf_token(request):
    return HttpResponse(csrf.get_token(request))


class GraphQLView(_GraphQLView):
    pass
