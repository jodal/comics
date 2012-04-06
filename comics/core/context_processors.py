from django.conf import settings
from django.contrib.sites.models import RequestSite, Site

from comics.core.models import Comic


def site_settings(request):
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    return {
        'site_title': site.name,
        'google_analytics_code': settings.COMICS_GOOGLE_ANALYTICS_CODE,
    }


def all_comics(request):
    return {
        'all_comics': Comic.objects.sort_by_name(),
    }
