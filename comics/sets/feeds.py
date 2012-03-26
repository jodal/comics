import datetime

from django.conf import settings
from django.contrib.sites.models import RequestSite, Site
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed

from comics.core.models import Release
from comics.sets.models import Set
from comics.core.utils.comic_releases import add_images

class NamedSetFeed(Feed):
    feed_type = Atom1Feed
    title_template = 'feeds/release-title.html'
    description_template = 'feeds/release-content.html'

    def get_object(self, request, namedset):
        if Site._meta.installed:
            self._site = Site.objects.get_current()
        else:
            self._site = RequestSite(request)
        return Set.objects.get(name=namedset)

    def title(self, obj):
        return '%s: Set: %s' % (self._site.name, obj.name)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def items(self, obj):
        from_date = datetime.date.today() \
            - datetime.timedelta(settings.COMICS_MAX_DAYS_IN_FEED)
        releases = Release.objects.select_related(depth=1).filter(
            comic__set=obj, pub_date__gte=from_date).order_by('-pub_date')
        add_images(releases)
        return releases

    def item_pubdate(self, item):
        return item.fetched

    def item_author_name(self):
        return self._site.name

    def item_copyright(self, item):
        return item.comic.rights
