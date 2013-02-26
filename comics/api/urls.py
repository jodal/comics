from django.conf.urls import include, patterns

from tastypie.api import Api

from comics.api.resources import (
    UsersResource, ComicsResource, ImagesResource, ReleasesResource,
    SubscriptionsResource)

v1_api = Api(api_name='v1')
v1_api.register(UsersResource())
v1_api.register(ComicsResource())
v1_api.register(ImagesResource())
v1_api.register(ReleasesResource())
v1_api.register(SubscriptionsResource())

urlpatterns = patterns('',
    (r'', include(v1_api.urls)),
)
