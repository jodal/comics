from __future__ import absolute_import

from django.conf import settings
from django.conf.urls import include, patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Robots not welcome
    (r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),

    # User accounts management
    (r'^account/', include('comics.accounts.urls')),

    # API
    (r'^api/', include('comics.api.urls')),

    # Help, about and feedback
    (r'^help/', include('comics.help.urls')),

    # Comic crawler status
    (r'^status/', include('comics.status.urls')),

    # Django admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # Comics browsing. Must be last one included.
    (r'^', include('comics.browser.urls')),
)

# Let Django host media if doing local development on runserver
if not settings.MEDIA_URL.startswith('http'):
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += staticfiles_urlpatterns()
