from __future__ import absolute_import

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from django.views.static import serve


urlpatterns = [
    # Robots not welcome
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),

    # User accounts management
    url(r'^account/', include('comics.accounts.urls')),

    # API
    url(r'^api/', include('comics.api.urls')),

    # Help, about and feedback
    url(r'^help/', include('comics.help.urls')),

    # Comic crawler status
    url(r'^status/', include('comics.status.urls')),

    # Django admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),

    # Comics browsing. Must be last one included.
    url(r'^', include('comics.browser.urls')),
]

# Let Django host media if doing local development on runserver
if not settings.MEDIA_URL.startswith('http'):
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

urlpatterns += staticfiles_urlpatterns()
