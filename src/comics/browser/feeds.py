import datetime
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, cast
from urllib.parse import urljoin, urlsplit

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import feedgenerator, timezone
from django.utils.formats import date_format

from comics.core.models import Comic, Release
from comics.core.querysets import ReleaseQuerySet

if TYPE_CHECKING:
    from comics.accounts.models import UserProfile
    from comics.accounts.typing import ComicsUser


def _get_profile(request: HttpRequest) -> "UserProfile":
    user = get_object_or_404(
        User,
        comics_profile__secret_key=request.GET.get("key"),
        is_active=True,
    )
    return cast("ComicsUser", user).comics_profile


def _absolute_url(path: str) -> str:
    # By returning absolute URLs, we bypass the syndication framework's own
    # absolutizing of URLs, which is based on the domain of the default Site
    # object in the database instead of our settings.
    site_url: str = settings.COMICS_SITE_URL
    return urljoin(site_url, path)


def _recent_releases(releases: ReleaseQuerySet) -> ReleaseQuerySet:
    from_time = timezone.now() - datetime.timedelta(
        days=settings.COMICS_MAX_DAYS_IN_FEED
    )
    return releases.filter(fetched__gte=from_time).order_by("-fetched")


class ReleaseFeed[ObjectT](Feed[Release, ObjectT]):
    """Things common for all Atom feeds of comic releases.

    Note that feed instances are created once at URLconf import time and
    shared between all requests, so all per-request state must be carried by
    the object returned by :meth:`get_object`.
    """

    feed_type = feedgenerator.Atom1Feed
    author_name = settings.COMICS_SITE_TITLE

    def item_title(self, item: Release) -> str:
        return f"{item.comic.name} published {date_format(item.pub_date)}"

    def item_updateddate(self, item: Release) -> datetime.datetime:
        return item.fetched

    def item_copyright(self, item: Release) -> str:
        return item.comic.rights

    def item_link(self, item: Release) -> str:
        return _absolute_url(item.get_absolute_url())

    def item_guid(self, item: Release) -> str:
        # A tag URI (RFC 4151), unlike the release's URL, stays unchanged if
        # the site changes domain or URL scheme, and is unique even if the
        # same comic gets multiple releases on the same day.
        site_url: str = settings.COMICS_SITE_URL
        authority = urlsplit(site_url).hostname
        return f"tag:{authority},{item.pub_date.isoformat()}:releases/{item.pk}"

    def item_description(self, item: Release) -> str:
        return render_to_string("browser/release_feed_summary.html", {"release": item})


class MyComicsFeed(ReleaseFeed["UserProfile"]):
    """Atom feed of releases from my comics"""

    def get_object(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> "UserProfile":
        return _get_profile(request)

    def title(self, obj: "UserProfile") -> str:
        return "My comics"

    def link(self, obj: "UserProfile") -> str:
        return _absolute_url(reverse("mycomics_latest"))

    def feed_url(self, obj: "UserProfile") -> str:
        return urljoin(
            _absolute_url(reverse("mycomics_feed")),
            f"?key={obj.secret_key}",
        )

    def items(self, obj: "UserProfile") -> ReleaseQuerySet:
        releases = Release.objects.select_related().filter(comic__in=obj.comics.all())
        return _recent_releases(releases)


@dataclass
class ComicForProfile:
    comic: Comic
    profile: "UserProfile"


class OneComicFeed(ReleaseFeed[ComicForProfile]):
    """Atom feed of releases of a single comic"""

    def get_object(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> ComicForProfile:
        return ComicForProfile(
            comic=get_object_or_404(Comic, slug=kwargs["comic_slug"]),
            profile=_get_profile(request),
        )

    def title(self, obj: ComicForProfile) -> str:
        return f"Comics from {obj.comic.name}"

    def link(self, obj: ComicForProfile) -> str:
        return _absolute_url(
            reverse("comic_latest", kwargs={"comic_slug": obj.comic.slug})
        )

    def feed_url(self, obj: ComicForProfile) -> str:
        return urljoin(
            _absolute_url(reverse("comic_feed", kwargs={"comic_slug": obj.comic.slug})),
            f"?key={obj.profile.secret_key}",
        )

    def items(self, obj: ComicForProfile) -> ReleaseQuerySet:
        releases = Release.objects.select_related().filter(comic=obj.comic)
        return _recent_releases(releases)
