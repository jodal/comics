from __future__ import annotations

from typing import TYPE_CHECKING, Self

from comics.core.querysets import BaseQuerySet

if TYPE_CHECKING:
    from django.contrib.auth.models import User

    from comics.accounts.models import Subscription, UserProfile  # noqa: F401
    from comics.core.models import Comic


class UserProfileQuerySet(BaseQuerySet["UserProfile"]):
    pass


class SubscriptionQuerySet(BaseQuerySet["Subscription"]):
    def for_user(self, user: User, /) -> Self:
        return self.filter(userprofile__user=user)

    def for_comic(self, comic: Comic, /) -> Self:
        return self.filter(comic=comic)
