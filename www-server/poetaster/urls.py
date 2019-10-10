from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from core.views import GraphQLView, serve_csrf_token
from schema import schema


urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^csrf/$', serve_csrf_token, name='csrf'),
    url(r'^', GraphQLView.as_view(
        schema=schema,
        graphiql=settings.DEBUG
    )),
]
