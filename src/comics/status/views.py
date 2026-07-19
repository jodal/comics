from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING, cast

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render

from comics.aggregator.utils import get_comic_schedule
from comics.core.models import Comic, Release

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest, HttpResponse

    class StatusComic(Comic):
        """A comic in the status timeline, as seen by type checkers.

        Adds the queryset annotation and the extra attribute set by the view
        for use in the template.
        """

        last_pub_date: dt.date | None
        days_since_last_release: int

    # The CSS classes, the date, and the release fetched that day, if any.
    TimelineCell = tuple[set[str], dt.date, Release | None]


@login_required
def status(request: HttpRequest, num_days: int = 21) -> HttpResponse:
    today = dt.date.today()
    last = today - dt.timedelta(days=num_days)

    releases = Release.objects.for_active_comics().published_since(last)
    releases = releases.select_related().order_by("comic__slug").distinct()

    release_by_comic_and_day: dict[tuple[int, int], Release] = {}
    for release in releases:
        day_num = (today - release.pub_date).days
        release_by_comic_and_day[(release.comic_id, day_num)] = release

    comics = cast(
        "QuerySet[StatusComic]",
        Comic.objects.active()
        .annotate(last_pub_date=Max("release__pub_date"))
        .order_by("last_pub_date"),
    )

    timeline: dict[Comic, list[TimelineCell]] = {}

    for comic in comics:
        if comic.last_pub_date:
            comic.days_since_last_release = (today - comic.last_pub_date).days
        else:
            comic.days_since_last_release = 1000

        schedule = get_comic_schedule(comic)
        cells: list[TimelineCell] = []

        for i in range(num_days + 1):
            day = today - dt.timedelta(days=i)
            classes: set[str] = set()

            if not schedule:
                classes.add("unscheduled")
            elif int(day.strftime("%w")) in schedule:
                classes.add("scheduled")

            days_release = release_by_comic_and_day.get((comic.pk, i))
            if days_release is not None:
                classes.add("fetched")

            cells.append((classes, day, days_release))

        timeline[comic] = cells

    days = [today - dt.timedelta(days=i) for i in range(num_days + 1)]

    return render(
        request,
        "status/status.html",
        {"active": {"status": True}, "days": days, "timeline": timeline},
    )
