import datetime

from django.conf import settings
from django.contrib.sites.models import RequestSite, Site
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed

from comics.accounts.models import UserProfile
from comics.core.models import Comic, Release
from comics.sets.models import UserSet


class MyComicsFeed(Feed):
    feed_type = Atom1Feed
    title_template = 'feeds/release_title.html'
    description_template = 'feeds/release_content.html'

    def get_object(self, request):
        if Site._meta.installed:
            self._site = Site.objects.get_current()
        else:
            self._site = RequestSite(request)

        try:
            user_profile = UserProfile.objects.get(
                secret_key=request.GET.get('key', None))
            if not user_profile.user.is_active:
                raise FeedDoesNotExist
            (user_set, _) = UserSet.objects.get_or_create(
                user=user_profile.user)
            return user_set
        except UserProfile.DoesNotExist:
            raise FeedDoesNotExist

    def title(self, user_set):
        return '%s for %s' % (self._site.name, user_set.user.email)

    def link(self, user_set):
        if not user_set:
            raise FeedDoesNotExist
        return user_set.get_absolute_url()

    def items(self, user_set):
        return Release.objects.select_related(depth=1).filter(
            comic__userset=user_set).order_by('-fetched')[:500]

    def item_pubdate(self, item):
        return item.fetched

    def item_author_name(self):
        return self._site.name

    def item_copyright(self, item):
        return item.comic.rights


class OneComicFeed(Feed):
    feed_type = Atom1Feed
    title_template = 'feeds/release_title.html'
    description_template = 'feeds/release_content.html'

    def get_object(self, request, comic_slug):
        if Site._meta.installed:
            self._site = Site.objects.get_current()
        else:
            self._site = RequestSite(request)

        try:
            user_profile = UserProfile.objects.get(
                secret_key=request.GET.get('key', None))
            if not user_profile.user.is_active:
                raise FeedDoesNotExist
        except UserProfile.DoesNotExist:
            raise FeedDoesNotExist

        return Comic.objects.get(slug=comic_slug)

    def title(self, comic):
        return '%s: %s' % (self._site.name, comic.name)

    def link(self, comic):
        if not comic:
            raise FeedDoesNotExist
        return comic.get_absolute_url()

    def items(self, comic):
        from_date = datetime.date.today() \
            - datetime.timedelta(settings.COMICS_MAX_DAYS_IN_FEED)
        return comic.release_set.select_related(depth=1).filter(
            pub_date__gte=from_date).order_by('-pub_date')

    def item_pubdate(self, item):
        return item.fetched

    def item_author_name(self):
        return self._site.name

    def item_copyright(self, item):
        return item.comic.rights
