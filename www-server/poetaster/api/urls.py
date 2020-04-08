from django.conf.urls import url, include

from django.views.decorators.csrf import csrf_exempt

from .v1.views import APIView as APIViewV1

versioned_urlpatterns = [
    url(r'v1', csrf_exempt(APIViewV1.as_view()))
]

urlpatterns = [
    url(r'graphql', include(versioned_urlpatterns))
]
