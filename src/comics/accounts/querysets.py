from __future__ import annotations

from typing import TYPE_CHECKING

from comics.core.querysets import BaseQuerySet

if TYPE_CHECKING:
    from comics.accounts.models import Subscription, UserProfile  # noqa: F401


class UserProfileQuerySet(BaseQuerySet["UserProfile"]):
    pass


class SubscriptionQuerySet(BaseQuerySet["Subscription"]):
    pass
