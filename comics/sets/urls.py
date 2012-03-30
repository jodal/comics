from django.conf.urls.defaults import patterns, url

from comics.sets import views

urlpatterns = patterns('',
    # User-associated comic sets
    url(r'^import/$',
        views.user_set_import_named_set, name='namedset-import'),
)
