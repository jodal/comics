from __future__ import absolute_import

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

from comics.core.feeds import ComicFeed
from comics.core.urls import COMIC
from comics.sets.feeds import SetFeed
from comics.sets.urls import SET

urlpatterns = patterns('',
    # Comic core
    (r'^', include('comics.core.urls')),

    # Comic sets
    (r'^s/', include('comics.sets.urls')),

    # Feedback app
    (r'^feedback/', include('comics.feedback.urls')),

    # User handling
    (r'^accounts/', include('comics.accounts.urls')),

    # Comic feeds
    url(r'^feeds/c/%s/$' % (COMIC,), ComicFeed(), name='comic-feed'),
    url(r'^feeds/s/%s/$' % (SET,), SetFeed(), name='set-feed'),

    # Django admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

# Let Django host media if doing local development on runserver
if not settings.MEDIA_URL.startswith('http'):
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += staticfiles_urlpatterns()
