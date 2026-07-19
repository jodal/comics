from __future__ import annotations

from typing import TYPE_CHECKING, Self, cast

from django.db import models
from django.db.models.functions import Lower

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

    def sort_by_name(self) -> Self:
        return self.order_by(Lower("name"))


class ReleaseQuerySet(BaseQuerySet["Release"]):
    pass


class ImageQuerySet(BaseQuerySet["Image"]):
    pass
