from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django_stubs_ext.db.models import TypedModelMeta

if TYPE_CHECKING:
    from comics.core.models import Comic  # noqa: F401


@receiver(models.signals.post_save, sender=User)
def create_user_profile(
    sender: type[User],
    instance: User,
    created: bool,
    **kwargs: Any,
) -> None:
    if created:
        UserProfile.objects.create(user=instance)


def make_secret_key() -> str:
    return uuid.uuid4().hex


class UserProfile(models.Model):
    user = models.OneToOneField["UserProfile", "User"](
        "auth.User",
        on_delete=models.CASCADE,
        related_name="comics_profile",
    )
    secret_key = models.CharField[str, str](
        max_length=32,
        blank=False,
        default=make_secret_key,
        help_text="Secret key for feed and API access",
    )
    comics = models.ManyToManyField["UserProfile", "Comic"](
        "core.Comic",
        through="Subscription",
    )

    class Meta(TypedModelMeta):
        db_table = "comics_user_profile"
        verbose_name = "comics profile"

    def __str__(self) -> str:
        return "Comics profile for %s" % self.user.email

    def generate_new_secret_key(self) -> None:
        self.secret_key = make_secret_key()


class Subscription(models.Model):
    userprofile = models.ForeignKey["Subscription", "UserProfile"](
        "UserProfile",
        on_delete=models.CASCADE,
    )
    comic = models.ForeignKey["Subscription", "Comic"](
        "core.Comic",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "comics_user_profile_comics"

    def __str__(self):
        return f"Subscription for {self.userprofile.user.email} to {self.comic.slug}"
