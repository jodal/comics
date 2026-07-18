from django.urls import path

from comics.api.views import api

urlpatterns = [
    path("v1/", api.urls),
]
