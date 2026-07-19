from django.conf import settings
from django.http import HttpRequest


def site_settings(request: HttpRequest) -> dict[str, str]:
    return {
        "site_title": settings.COMICS_SITE_TITLE,
        "google_analytics_code": settings.COMICS_GOOGLE_ANALYTICS_CODE,
    }
