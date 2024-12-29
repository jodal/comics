import re

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView
from django.views.static import serve

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


# Let Django host media if nothing in front of it handles the request.
if not settings.MEDIA_URL.startswith("http"):
    urlpatterns += [
        re_path(
            r"^%s(?P<path>.*)$" % re.escape(settings.MEDIA_URL.lstrip("/")),
            serve,
            kwargs={"document_root": settings.MEDIA_ROOT},
        ),
    ]


# Include debug_toolbar during development
if settings.DEBUG:
    try:
        from debug_toolbar.toolbar import debug_toolbar_urls
    except ImportError:
        pass
    else:
        urlpatterns += debug_toolbar_urls()
