from django.conf import settings
from django.db.models import Max

from comics.core.models import Comic

def site_settings(request):
    return {
        'site_title': settings.COMICS_SITE_TITLE,
        'site_tagline': settings.COMICS_SITE_TAGLINE,
        'google_analytics_code': settings.COMICS_GOOGLE_ANALYTICS_CODE,
    }

def all_comics(request):
    all_comics = Comic.objects.sort_by_name()
    all_comics = all_comics.annotate(Max('release__fetched'))
    return {'all_comics': all_comics}
