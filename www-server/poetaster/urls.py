from django.conf.urls import url, include
from django.contrib import admin

from api.urls import urlpatterns as api_urlpatterns

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^', include(api_urlpatterns))
]
