from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    # Robots not welcome
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    # Core, metrics, etc.
    path("core/", include("comics.core.urls")),
    # User accounts management
    path("accounts/", include("allauth.urls")),
    path("invitations/", include("invitations.urls", namespace="invitations")),
    path("me/", include("comics.accounts.urls")),
    # API
    path("api/", include("comics.api.urls")),
    # Help, about and feedback
    path("help/", include("comics.help.urls")),
    # Comic crawler status
    path("status/", include("comics.status.urls")),
    # Django admin
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    # Comics browsing. Must be last one included.
    path("", include("comics.browser.urls")),
]


# Let Django host media if doing local development on runserver
if not settings.MEDIA_URL.startswith("http"):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Include debug_toolbar during development
if settings.DEBUG:
    try:
        from debug_toolbar.toolbar import debug_toolbar_urls
    except ImportError:
        pass
    else:
        urlpatterns += debug_toolbar_urls()


urlpatterns += static(settings.STATIC_URL)
