import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed

from comics.core.models import Release
from comics.sets.models import NamedSet
from comics.core.utils.comic_releases import add_images

class NamedSetFeed(Feed):
    feed_type = Atom1Feed
    item_author_name = Site.objects.get_current().name
    title_template = 'feeds/release-title.html'
    description_template = 'feeds/release-content.html'

    def get_object(self, request, namedset):
        return NamedSet.objects.get(name=namedset)

    def title(self, obj):
        return '%s: Set: %s' % (Site.objects.get_current().name, obj.name)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def items(self, obj):
        from_date = datetime.date.today() \
            - datetime.timedelta(settings.COMICS_MAX_DAYS_IN_FEED)
        releases = Release.objects.select_related(depth=1
            ).filter(comic__named_set=obj, pub_date__gte=from_date
            ).order_by('-pub_date')
        add_images(releases)
        return releases

    def item_pubdate(self, item):
        return item.fetched

    def item_copyright(self, item):
        return item.comic.rights
