from django.urls import include, path
from tastypie.api import Api

from comics.api.resources import (
    ComicsResource,
    ImagesResource,
    ReleasesResource,
    SubscriptionsResource,
    UsersResource,
)

v1_api = Api(api_name="v1")
v1_api.register(UsersResource())
v1_api.register(ComicsResource())
v1_api.register(ImagesResource())
v1_api.register(ReleasesResource())
v1_api.register(SubscriptionsResource())

urlpatterns = [
    path("", include(v1_api.urls)),
]
