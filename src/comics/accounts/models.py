from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, ClassVar

from django.db import models

from comics.accounts.querysets import SubscriptionQuerySet, UserProfileQuerySet
from comics.core.models import BaseModel

if TYPE_CHECKING:
    from django.contrib.auth.models import User  # noqa: F401

    from comics.core.models import Comic  # noqa: F401


def make_secret_key() -> str:
    return uuid.uuid4().hex


class UserProfile(BaseModel):
    user = models.OneToOneField["User"](
        "auth.User",
        on_delete=models.CASCADE,
        related_name="comics_profile",
    )
    secret_key = models.CharField[str](
        max_length=32,
        blank=False,
        default=make_secret_key,
        help_text="Secret key for feed and API access",
    )
    comics = models.ManyToManyField["Comic", "Subscription"](
        "core.Comic",
        through="Subscription",
    )

    objects: ClassVar[UserProfileQuerySet] = UserProfileQuerySet.as_manager()

    class Meta(BaseModel.Meta):
        db_table = "comics_user_profile"
        verbose_name = "comics profile"

    def __str__(self) -> str:
        return f"Comics profile for {self.user.email}"


class Subscription(BaseModel):
    userprofile = models.ForeignKey["UserProfile"](
        "UserProfile",
        on_delete=models.CASCADE,
    )
    comic = models.ForeignKey["Comic"](
        "core.Comic",
        on_delete=models.CASCADE,
    )
    comic_id: int

    objects: ClassVar[SubscriptionQuerySet] = SubscriptionQuerySet.as_manager()

    class Meta(BaseModel.Meta):
        db_table = "comics_user_profile_comics"
        constraints = [
            models.UniqueConstraint(
                fields=["userprofile", "comic"],
                name="unique_subscription",
            )
        ]

    def __str__(self) -> str:
        return f"Subscription for {self.userprofile.user.email} to {self.comic.slug}"
