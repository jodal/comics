from django.conf import settings


def site_settings(request):
    return {
        "site_title": settings.COMICS_SITE_TITLE,
        "google_analytics_code": settings.COMICS_GOOGLE_ANALYTICS_CODE,
    }
