import datetime

from django.contrib.sites.models import RequestSite, Site
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.http import HttpResponseForbidden
from django.utils.feedgenerator import Atom1Feed

from comics.accounts.models import UserProfile
from comics.core.models import Release
from comics.sets.models import UserSet

class UserSetFeed(Feed):
    feed_type = Atom1Feed
    title_template = 'feeds/release-title.html'
    description_template = 'feeds/release-content.html'

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
            comic__userset=user_set).order_by('-fetched')[:1000]

    def item_pubdate(self, item):
        return item.fetched

    def item_author_name(self):
        return self._site.name

    def item_copyright(self, item):
        return item.comic.rights
