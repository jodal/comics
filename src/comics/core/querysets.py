from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING, Self, cast

from django.conf import settings
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone

if TYPE_CHECKING:
    from comics.core.models import Comic, Image, Release  # noqa: F401


class BaseQuerySet[M: models.Model](models.QuerySet[M]):
    @classmethod
    def as_manager(cls) -> Self:  # pyright: ignore[reportIncompatibleMethodOverride]
        # The return type is annotated as `Self` even though a
        # `models.Manager` subclass is returned: all queryset methods are
        # copied over to the manager, and those are the methods that
        # application code interacts with.
        return cast("Self", super().as_manager())


class ComicQuerySet(BaseQuerySet["Comic"]):
    def active(self) -> Self:
        return self.filter(active=True)

    def inactive(self) -> Self:
        return self.filter(active=False)

    def for_slug(self, slug: str, /) -> Self:
        return self.filter(slug=slug)

    def sort_by_name(self) -> Self:
        return self.order_by(Lower("name"))


class ReleaseQuerySet(BaseQuerySet["Release"]):
    def for_comics(self, *comics: Comic) -> Self:
        return self.filter(comic__in=comics)

    def for_feed(self) -> Self:
        """The releases recently fetched enough to be in a feed, newest first."""
        from_time = timezone.now() - dt.timedelta(days=settings.COMICS_MAX_DAYS_IN_FEED)
        return self.filter(fetched__gte=from_time).order_by("-fetched")

    def first_pub_date(self) -> dt.date | None:
        """The oldest publication date, if any releases exist."""
        return self.values_list("pub_date", flat=True).order_by("pub_date").first()

    def last_pub_date(self) -> dt.date | None:
        """The newest publication date, if any releases exist."""
        return self.values_list("pub_date", flat=True).order_by("-pub_date").first()

    def last_pub_dates(self, count: int, /) -> list[dt.date]:
        """The ``count`` newest publication dates, newest first."""
        return list(
            self.values_list("pub_date", flat=True).order_by("-pub_date")[:count]
        )


class ImageQuerySet(BaseQuerySet["Image"]):
    pass
