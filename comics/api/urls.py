from django.conf.urls.defaults import include, patterns

from tastypie.api import Api

from comics.api.resources import ComicsResource, ImagesResource, ReleasesResource

v1_api = Api(api_name='v1')
v1_api.register(ComicsResource())
v1_api.register(ImagesResource())
v1_api.register(ReleasesResource())

urlpatterns = patterns('',
    (r'', include(v1_api.urls)),
)
