from django.conf import settings

from comics.core.models import Comic


def site_settings(request):
    return {
        "site_title": settings.COMICS_SITE_TITLE,
        "google_analytics_code": settings.COMICS_GOOGLE_ANALYTICS_CODE,
    }


def all_comics(request):
    return {
        "all_comics": Comic.objects.sort_by_name(),
    }
