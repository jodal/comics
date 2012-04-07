from __future__ import absolute_import

from django.conf import settings
from django.conf.urls.defaults import include, patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    # Comic core
    (r'^', include('comics.core.urls')),

    # User handling
    (r'^account/', include('comics.accounts.urls')),

    # Feedback app
    (r'^feedback/', include('comics.feedback.urls')),

    # Status app
    (r'^status/', include('comics.status.urls')),

    # Django admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # Comics browsing
    (r'^', include('comics.browser.urls')),
)

# Let Django host media if doing local development on runserver
if not settings.MEDIA_URL.startswith('http'):
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += staticfiles_urlpatterns()
