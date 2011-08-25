import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed

from comics.core.models import Comic

class ComicFeed(Feed):
    feed_type = Atom1Feed
    item_author_name = Site.objects.get_current().name
    title_template = 'feeds/release-title.html'
    description_template = 'feeds/release-content.html'

    def get_object(self, request, comic):
        return Comic.objects.get(slug=comic)

    def title(self, obj):
        return '%s: %s' % (Site.objects.get_current().name, obj.name)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def items(self, obj):
        from_date = datetime.date.today() \
            - datetime.timedelta(settings.COMICS_MAX_DAYS_IN_FEED)
        return obj.release_set.select_related(depth=1).filter(
            pub_date__gte=from_date).order_by('-pub_date')

    def item_pubdate(self, item):
        return item.fetched

    def item_copyright(self, item):
        return item.comic.rights
