from __future__ import absolute_import

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from comics.core.feeds import ComicFeed
from comics.sets.feeds import SetFeed

feeds = {
    'c': ComicFeed,
    's': SetFeed,
}

urlpatterns = patterns('',
    # Comic core
    (r'^', include('comics.core.urls')),

    # Comic sets
    (r'^s/', include('comics.sets.urls')),

    # Feedback app
    (r'^feedback/', include('comics.feedback.urls')),

    # Comic feeds
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}, name='feeds'),

    # Django admin
    (r'^admin/media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.ADMIN_MEDIA_ROOT}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)

# Comic search
if 'comics.search' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^search/', include('comics.search.urls')),
    )

# Let Django host media if doing local development on runserver
if not settings.MEDIA_URL.startswith('http'):
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
