from __future__ import annotations

import datetime as dt
import json
from typing import TYPE_CHECKING, Any, cast

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (
    DayArchiveView,
    ListView,
    MonthArchiveView,
    RedirectView,
    TemplateView,
    TodayArchiveView,
    View,
)
from django.views.generic.base import TemplateResponseMixin

from comics.core.models import Comic, Release

if TYPE_CHECKING:
    from comics.accounts.typing import AuthenticatedHttpRequest, ComicsUser
    from comics.core.querysets import ComicQuerySet, ReleaseQuerySet


@login_required
def comics_list(request: AuthenticatedHttpRequest) -> HttpResponse:
    return render(
        request,
        "browser/comics_list.html",
        {
            "active": {"comics_list": True},
            "active_comics": Comic.objects.active().sort_by_name(),
            "inactive_comics": Comic.objects.inactive().sort_by_name(),
            "my_comics": request.user.comics_profile.comics.all(),
        },
    )


class ComicMixin(View):
    """Things common for *all* views of comics"""

    _comic: Comic

    @property
    def comic(self) -> Comic:
        if not hasattr(self, "_comic"):
            self._comic = get_object_or_404(
                Comic.objects.for_slug(self.kwargs["comic_slug"])
            )
        return self._comic

    def get_user(self) -> ComicsUser:
        # All views using this mixin require a logged-in user.
        return cast("ComicsUser", self.request.user)

    def get_my_comics(self) -> ComicQuerySet:
        # The related manager derives from Comic's default manager, so all()
        # returns a ComicQuerySet, which the stubs cannot know.
        return cast("ComicQuerySet", self.get_user().comics_profile.comics.all())


class ReleaseMixin(LoginRequiredMixin, TemplateResponseMixin, ComicMixin):
    """Things common for *all* views of comic releases"""

    allow_future = True
    template_name = "browser/release_list.html"

    context: dict[str, Any]

    def render_to_response(
        self,
        context: dict[str, Any],
        **kwargs: Any,
    ) -> HttpResponse:
        # We hook into render_to_response() instead of get_context_data()
        # because the date based views only populate the context with
        # date-related information right before render_to_response() is called.
        context.update(self.get_release_context_data(context))
        return super().render_to_response(context, **kwargs)

    def get_release_context_data(self, context: dict[str, Any]) -> dict[str, Any]:
        # The methods called later in this method assumes that ``self.context``
        # contains what is already ready to be made available for the template.
        self.context = context

        return {
            "my_comics": self.get_my_comics(),
            "active": {"comics": True},
            "object_type": self.get_object_type(),
            "view_type": self.get_view_type(),
            "title": self.get_title(),
            "subtitle": self.get_subtitle(),
            "latest_url": self.get_latest_url(),
            "today_url": self.get_today_url(),
            "day_url": self.get_day_url(),
            "month_url": self.get_month_url(),
            "feed_url": self.get_feed_url(),
            "feed_title": self.get_feed_title(),
            "first_url": self.get_first_url(),
            "prev_url": self.get_prev_url(),
            "next_url": self.get_next_url(),
            "last_url": self.get_last_url(),
        }

    def get_object_type(self) -> str | None:
        return None

    def get_view_type(self) -> str | None:
        return None

    def get_title(self) -> str | None:
        return None

    def get_subtitle(self) -> str | None:
        return None

    def get_latest_url(self) -> str | None:
        return None

    def get_today_url(self) -> str | None:
        return None

    def get_day_url(self) -> str | None:
        return None

    def get_month_url(self) -> str | None:
        return None

    def get_feed_url(self) -> str | None:
        return None

    def get_feed_title(self) -> str | None:
        return None

    def get_first_url(self) -> str | None:
        return None

    def get_prev_url(self) -> str | None:
        return None

    def get_next_url(self) -> str | None:
        return None

    def get_last_url(self) -> str | None:
        return None


class ReleaseLatestView(ReleaseMixin, ListView):
    """Things common for all *latest* views"""

    def get_subtitle(self) -> str | None:
        return "Latest releases"

    def get_view_type(self) -> str | None:
        return "latest"


class ReleaseDateMixin(ReleaseMixin):
    """Things common for all *date based* views"""

    date_field: str | None = "pub_date"
    month_format = "%m"


class ReleaseDayArchiveView(ReleaseDateMixin, DayArchiveView):
    """Things common for all *day* views"""

    def get_view_type(self) -> str | None:
        return "day"

    def get_subtitle(self) -> str | None:
        day: dt.date = self.context["day"]
        return day.strftime("%A %d %B %Y").replace(" 0", " ")


class ReleaseTodayArchiveView(ReleaseDateMixin, TodayArchiveView):
    """Things common for all *today* views"""

    def get_view_type(self) -> str | None:
        return "today"

    def get_subtitle(self) -> str | None:
        return "Today"


class ReleaseMonthArchiveView(ReleaseDateMixin, MonthArchiveView):
    """Things common for all *month* views"""

    def get_view_type(self) -> str | None:
        return "month"

    def get_subtitle(self) -> str | None:
        month: dt.date = self.context["month"]
        return month.strftime("%B %Y")


class MyComicsMixin(ReleaseMixin):
    """Things common for all views of *my comics*"""

    def get_queryset(self) -> ReleaseQuerySet:
        return (
            Release.objects.select_related()
            .for_comics(*self.get_my_comics())
            .order_by("pub_date")
        )

    def get_object_type(self) -> str | None:
        return "mycomics"

    def get_title(self) -> str | None:
        return "My comics"

    def get_latest_url(self) -> str | None:
        return reverse("mycomics_latest")

    def get_today_url(self) -> str | None:
        return reverse("mycomics_today")

    _last_pub_date: dt.date | None

    def _get_last_pub_date(self) -> dt.date | None:
        if not hasattr(self, "_last_pub_date"):
            self._last_pub_date = self.get_queryset().last_pub_date()
        return self._last_pub_date

    def get_day_url(self) -> str | None:
        last_date = self._get_last_pub_date()
        if last_date is None:
            return None
        return reverse(
            "mycomics_day",
            kwargs={
                "year": last_date.year,
                "month": last_date.month,
                "day": last_date.day,
            },
        )

    def get_month_url(self) -> str | None:
        last_month = self._get_last_pub_date()
        if last_month is None:
            return None
        return reverse(
            "mycomics_month",
            kwargs={"year": last_month.year, "month": last_month.month},
        )

    def get_feed_url(self) -> str | None:
        return "{}?key={}".format(
            reverse("mycomics_feed"),
            self.get_user().comics_profile.secret_key,
        )

    def get_feed_title(self) -> str | None:
        return "My comics"


class MyComicsHome(LoginRequiredMixin, RedirectView):
    """Redirects the home page to my comics"""

    permanent = True

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str:
        return reverse("mycomics_latest")


class MyComicsLatestView(MyComicsMixin, ReleaseLatestView):
    """View of the latest releases from my comics"""

    paginate_by = settings.COMICS_MAX_RELEASES_PER_PAGE

    def get_queryset(self) -> ReleaseQuerySet:
        releases = super().get_queryset()
        return releases.order_by("-fetched")

    def get_first_url(self) -> str | None:
        page = self.context["page_obj"]
        if page.number != page.paginator.num_pages:
            return reverse(
                "mycomics_latest_page_n",
                kwargs={"page": page.paginator.num_pages},
            )
        return None

    def get_prev_url(self) -> str | None:
        page = self.context["page_obj"]
        if page.has_next():
            return reverse(
                "mycomics_latest_page_n",
                kwargs={"page": page.next_page_number()},
            )
        return None

    def get_next_url(self) -> str | None:
        page = self.context["page_obj"]
        if page.has_previous():
            return reverse(
                "mycomics_latest_page_n",
                kwargs={"page": page.previous_page_number()},
            )
        return None

    def get_last_url(self) -> str | None:
        page = self.context["page_obj"]
        if page.number != 1:
            return reverse("mycomics_latest_page_n", kwargs={"page": 1})
        return None


class MyComicsNumReleasesSinceView(MyComicsLatestView):
    def get_num_releases_since(self) -> int:
        last_release_seen = get_object_or_404(Release, id=self.kwargs["release_id"])
        releases = super().get_queryset()
        return releases.fetched_after(last_release_seen.fetched).count()

    def render_to_response(
        self,
        context: dict[str, Any],
        **kwargs: Any,
    ) -> HttpResponse:
        data = json.dumps(
            {
                "since_release_id": int(self.kwargs["release_id"]),
                "num_releases": self.get_num_releases_since(),
                "seconds_to_next_check": settings.COMICS_BROWSER_REFRESH_INTERVAL,
            }
        )
        return HttpResponse(data, content_type="application/json")


class MyComicsDayView(MyComicsMixin, ReleaseDayArchiveView):
    """View of releases from my comics for a given day"""

    def get_first_url(self) -> str | None:
        first_date = self.get_queryset().first_pub_date()
        if first_date is not None and first_date < self.context["day"]:
            return reverse(
                "mycomics_day",
                kwargs={
                    "year": first_date.year,
                    "month": first_date.month,
                    "day": first_date.day,
                },
            )
        return None

    def get_prev_url(self) -> str | None:
        prev_date = self.get_previous_day(self.context["day"])
        if prev_date:
            return reverse(
                "mycomics_day",
                kwargs={
                    "year": prev_date.year,
                    "month": prev_date.month,
                    "day": prev_date.day,
                },
            )
        return None

    def get_next_url(self) -> str | None:
        next_date = self.get_next_day(self.context["day"])
        if next_date:
            return reverse(
                "mycomics_day",
                kwargs={
                    "year": next_date.year,
                    "month": next_date.month,
                    "day": next_date.day,
                },
            )
        return None

    def get_last_url(self) -> str | None:
        last_date = self.get_queryset().last_pub_date()
        if last_date is not None and last_date > self.context["day"]:
            return reverse(
                "mycomics_day",
                kwargs={
                    "year": last_date.year,
                    "month": last_date.month,
                    "day": last_date.day,
                },
            )
        return None


class MyComicsTodayView(MyComicsMixin, ReleaseTodayArchiveView):
    """View of releases from my comics for today"""

    allow_empty = True

    def get_prev_url(self) -> str | None:
        prev_date = self.get_previous_day(self.context["day"])
        if prev_date:
            return reverse(
                "mycomics_day",
                kwargs={
                    "year": prev_date.year,
                    "month": prev_date.month,
                    "day": prev_date.day,
                },
            )
        return None


class MyComicsMonthView(MyComicsMixin, ReleaseMonthArchiveView):
    """View of releases from my comics for a given month"""

    def get_first_url(self) -> str | None:
        first_month = self.get_queryset().first_pub_date()
        if first_month is not None and first_month < self.context["month"]:
            return reverse(
                "mycomics_month",
                kwargs={
                    "year": first_month.year,
                    "month": first_month.month,
                },
            )
        return None

    def get_prev_url(self) -> str | None:
        prev_month = self.context["previous_month"]
        if prev_month:
            return reverse(
                "mycomics_month",
                kwargs={"year": prev_month.year, "month": prev_month.month},
            )
        return None

    def get_next_url(self) -> str | None:
        next_month = self.context["next_month"]
        if next_month:
            return reverse(
                "mycomics_month",
                kwargs={"year": next_month.year, "month": next_month.month},
            )
        return None

    def get_last_url(self) -> str | None:
        last_month = self.get_queryset().last_pub_date()
        if last_month is not None and last_month > self.context["month"]:
            return reverse(
                "mycomics_month",
                kwargs={
                    "year": last_month.year,
                    "month": last_month.month,
                },
            )
        return None


class MyComicsYearView(LoginRequiredMixin, RedirectView):
    """Redirect anyone trying to view the full year to January"""

    permanent = True

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str:
        return reverse("mycomics_month", kwargs={"year": kwargs["year"], "month": "1"})


class OneComicMixin(ReleaseMixin):
    """Things common for all views of a single comic"""

    if TYPE_CHECKING:
        # Implemented by the subclasses combining this mixin with a date-based
        # Django view, which provides get_previous_day() and get_next_day().
        def get_current_day(self) -> dt.date | None: ...
        def get_previous_day(self, date: dt.date) -> dt.date | None: ...
        def get_next_day(self, date: dt.date) -> dt.date | None: ...

    def get_queryset(self) -> ReleaseQuerySet:
        return (
            Release.objects.select_related().for_comics(self.comic).order_by("pub_date")
        )

    def get_object_type(self) -> str | None:
        return "onecomic"

    def get_title(self) -> str | None:
        return self.comic.name

    def get_latest_url(self) -> str | None:
        return reverse("comic_latest", kwargs={"comic_slug": self.comic.slug})

    _recent_pub_dates: list[dt.date]

    def _get_recent_pub_dates(self) -> list[dt.date]:
        if not hasattr(self, "_recent_pub_dates"):
            self._recent_pub_dates = self.get_queryset().last_pub_dates(2)
        return self._recent_pub_dates

    def get_today_url(self) -> str | None:
        if dt.date.today() in self._get_recent_pub_dates():
            return reverse("comic_today", kwargs={"comic_slug": self.comic.slug})
        return None

    def get_day_url(self) -> str | None:
        try:
            last_pub_date = self._get_recent_pub_dates()[0]
            return reverse(
                "comic_day",
                kwargs={
                    "comic_slug": self.comic.slug,
                    "year": last_pub_date.year,
                    "month": last_pub_date.month,
                    "day": last_pub_date.day,
                },
            )
        except IndexError:
            return None

    def get_month_url(self) -> str | None:
        try:
            last_pub_date = self._get_recent_pub_dates()[0]
            return reverse(
                "comic_month",
                kwargs={
                    "comic_slug": self.comic.slug,
                    "year": last_pub_date.year,
                    "month": last_pub_date.month,
                },
            )
        except IndexError:
            return None

    def get_feed_url(self) -> str | None:
        return "{}?key={}".format(
            reverse("comic_feed", kwargs={"comic_slug": self.comic.slug}),
            self.get_user().comics_profile.secret_key,
        )

    def get_feed_title(self) -> str | None:
        return f"Comics from {self.comic.name}"

    def get_first_url(self) -> str | None:
        first_date = self.get_queryset().first_pub_date()
        current_day = self.get_current_day()
        if (
            first_date is not None
            and current_day is not None
            and first_date < current_day
        ):
            return reverse(
                "comic_day",
                kwargs={
                    "comic_slug": self.comic.slug,
                    "year": first_date.year,
                    "month": first_date.month,
                    "day": first_date.day,
                },
            )
        return None

    def get_prev_url(self) -> str | None:
        current_day = self.get_current_day()
        prev_date = (
            self.get_previous_day(current_day) if current_day is not None else None
        )
        if prev_date:
            return reverse(
                "comic_day",
                kwargs={
                    "comic_slug": self.comic.slug,
                    "year": prev_date.year,
                    "month": prev_date.month,
                    "day": prev_date.day,
                },
            )
        return None

    def get_next_url(self) -> str | None:
        current_day = self.get_current_day()
        next_date = self.get_next_day(current_day) if current_day is not None else None
        if next_date:
            return reverse(
                "comic_day",
                kwargs={
                    "comic_slug": self.comic.slug,
                    "year": next_date.year,
                    "month": next_date.month,
                    "day": next_date.day,
                },
            )
        return None

    def get_last_url(self) -> str | None:
        try:
            last_pub_date = self._get_recent_pub_dates()[0]
            current_day = self.get_current_day()
            if current_day is not None and last_pub_date > current_day:
                return reverse(
                    "comic_day",
                    kwargs={
                        "comic_slug": self.comic.slug,
                        "year": last_pub_date.year,
                        "month": last_pub_date.month,
                        "day": last_pub_date.day,
                    },
                )
        except IndexError:
            return None
        return None


class OneComicLatestView(OneComicMixin, ReleaseLatestView):
    """View of the latest release from a single comic"""

    paginate_by = 1

    def get_queryset(self) -> ReleaseQuerySet:
        releases = super().get_queryset()
        return releases.order_by("-fetched")

    def get_current_day(self) -> dt.date | None:
        try:
            return self._get_recent_pub_dates()[0]
        except IndexError:
            return None

    def get_previous_day(self, date: dt.date) -> dt.date | None:
        try:
            return self._get_recent_pub_dates()[1]
        except IndexError:
            return None

    def get_next_day(self, date: dt.date) -> dt.date | None:
        return None  # Nothing is newer than 'latest'


class OneComicDayView(OneComicMixin, ReleaseDayArchiveView):
    """View of the releases from a single comic for a given day"""

    def get_current_day(self) -> dt.date | None:
        day: dt.date = self.context["day"]
        return day


class OneComicTodayView(OneComicMixin, ReleaseTodayArchiveView):
    """View of the releases from a single comic for today"""

    def get_current_day(self) -> dt.date | None:
        day: dt.date = self.context["day"]
        return day


class OneComicMonthView(OneComicMixin, ReleaseMonthArchiveView):
    """View of the releases from a single comic for a given month"""

    def get_first_url(self) -> str | None:
        first_month = self.get_queryset().first_pub_date()
        if first_month is not None and first_month < self.context["month"]:
            return reverse(
                "comic_month",
                kwargs={
                    "comic_slug": self.comic.slug,
                    "year": first_month.year,
                    "month": first_month.month,
                },
            )
        return None

    def get_prev_url(self) -> str | None:
        prev_month = self.context["previous_month"]
        if prev_month:
            return reverse(
                "comic_month",
                kwargs={
                    "comic_slug": self.comic.slug,
                    "year": prev_month.year,
                    "month": prev_month.month,
                },
            )
        return None

    def get_next_url(self) -> str | None:
        next_month = self.context["next_month"]
        if next_month:
            return reverse(
                "comic_month",
                kwargs={
                    "comic_slug": self.comic.slug,
                    "year": next_month.year,
                    "month": next_month.month,
                },
            )
        return None

    def get_last_url(self) -> str | None:
        try:
            last_pub_date = self._get_recent_pub_dates()[0]
            if last_pub_date > self.context["month"]:
                return reverse(
                    "comic_month",
                    kwargs={
                        "comic_slug": self.comic.slug,
                        "year": last_pub_date.year,
                        "month": last_pub_date.month,
                    },
                )
        except IndexError:
            return None
        return None


class OneComicYearView(LoginRequiredMixin, RedirectView):
    """Redirect anyone trying to view the full year to January"""

    permanent = True

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str:
        return reverse(
            "comic_month",
            kwargs={
                "comic_slug": kwargs["comic_slug"],
                "year": kwargs["year"],
                "month": "1",
            },
        )


class OneComicWebsiteRedirect(LoginRequiredMixin, ComicMixin, TemplateView):
    template_name = "browser/comic_website.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["url"] = self.comic.url
        return context
