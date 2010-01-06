from django.conf import settings

from comics.core.models import Comic

def site_settings(request):
    return {
        'site_title': settings.COMICS_SITE_TITLE,
        'site_tagline': settings.COMICS_SITE_TAGLINE,
    }

def all_comics(request):
    return {'all_comics': Comic.objects.sort_by_name()}
