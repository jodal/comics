import datetime

from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed

from comics.core.models import Release
from comics.sets.models import Set

class SetFeed(Feed):
    feed_type = Atom1Feed
    item_author_name = settings.COMICS_SITE_TITLE
    title_template = 'feeds/release-title.html'
    description_template = 'feeds/release-content.html'

    def get_object(self, bits):
        if len(bits) != 1:
            raise Set.DoesNotExist
        return Set.objects.get(name=bits[0])

    def title(self, obj):
        return '%s: Set: %s' % (settings.COMICS_SITE_TITLE, obj.name)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def items(self, obj):
        from_date = datetime.date.today() \
            - datetime.timedelta(settings.COMICS_MAX_DAYS_IN_FEED)
        return Release.objects.select_related(depth=1).filter(comic__set=obj,
            pub_date__gte=from_date).order_by('-pub_date')

    def item_pubdate(self, item):
        return item.strip.fetched

    def item_copyright(self, item):
        return item.comic.rights
