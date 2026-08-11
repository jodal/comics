from __future__ import annotations

from typing import TYPE_CHECKING

from comics.accounts.models import Subscription

if TYPE_CHECKING:
    from comics.accounts.typing import ComicsUser
    from comics.core.models import Comic


class SubscriptionService:
    @staticmethod
    def subscribe(*, user: ComicsUser, comic: Comic) -> Subscription:
        """Subscribe the user to the comic, if they are not already."""
        subscription, _ = Subscription.objects.get_or_create(
            userprofile=user.comics_profile,
            comic=comic,
        )
        return subscription

    @staticmethod
    def unsubscribe(*, user: ComicsUser, comic: Comic) -> bool:
        """Unsubscribe the user from the comic.

        Returns whether the user was subscribed in the first place.
        """
        num_deleted, _ = Subscription.objects.for_user(user).for_comic(comic).delete()
        return num_deleted > 0
