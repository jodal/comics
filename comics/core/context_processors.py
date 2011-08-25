from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import Count, Max

from comics.core.models import Comic

def site_settings(request):
    return {
        'site_title': Site.objects.get_current().name,
        'google_analytics_code': settings.COMICS_GOOGLE_ANALYTICS_CODE,
    }

def all_comics(request):
    all_comics = Comic.objects.sort_by_name()
    all_comics = all_comics.annotate(Max('release__fetched'))
    all_comics = all_comics.annotate(Count('release'))

    return {'all_comics': all_comics}

