from django.conf.urls.defaults import include, patterns

from comics.api.resources import ComicResource

comic_resource = ComicResource()

urlpatterns = patterns('',
    (r'', include(comic_resource.urls)),
)
