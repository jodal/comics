from django.conf import settings
from django.core.cache import cache
from django.db.models import Count, Max

from comics.core.models import Comic

def site_settings(request):
    return {
        'site_title': settings.COMICS_SITE_TITLE,
        'site_tagline': settings.COMICS_SITE_TAGLINE,
        'google_analytics_code': settings.COMICS_GOOGLE_ANALYTICS_CODE,
    }

def all_comics(request):
    all_comics = cache.get('all_comics')

    if all_comics is None:
        all_comics = Comic.objects.sort_by_name()
        all_comics = all_comics.annotate(Max('release__fetched'))
        all_comics = all_comics.annotate(Count('release'))
        cache.set('all_comics', list(all_comics))

    return {'all_comics': all_comics}

