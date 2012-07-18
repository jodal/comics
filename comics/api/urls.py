from django.conf.urls.defaults import include, patterns

from tastypie.api import Api

from comics.api.resources import (
    UserResource, ComicsResource, ImagesResource, ReleasesResource,
    MyComicsResource, MyReleasesResource)

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ComicsResource())
v1_api.register(ImagesResource())
v1_api.register(ReleasesResource())
v1_api.register(MyComicsResource())
v1_api.register(MyReleasesResource())

urlpatterns = patterns('',
    (r'', include(v1_api.urls)),
)
