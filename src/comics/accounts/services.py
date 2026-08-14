from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.db import transaction
from invitations.utils import get_invitation_model

from comics.accounts.models import Subscription, UserProfile, make_secret_key
from comics.core.models import Comic

if TYPE_CHECKING:
    from collections.abc import Collection

    from django.contrib.auth.models import User
    from django.http import HttpRequest
    from invitations.models import Invitation

    from comics.accounts.typing import ComicsUser

logger = logging.getLogger("comics.accounts.services")


class UserProfileService:
    @staticmethod
    def create_for_user(*, user: User) -> UserProfile:
        """Give a newly created user their comics profile."""
        return UserProfile.objects.create(user=user)

    @staticmethod
    def regenerate_secret_key(*, user: ComicsUser) -> UserProfile:
        """Replace the user's secret key for feed and API access."""
        profile = user.comics_profile
        profile.secret_key = make_secret_key()
        profile.save()
        return profile


class InvitationService:
    @staticmethod
    @transaction.atomic
    def invite(
        *,
        inviter: ComicsUser,
        email: str,
        request: HttpRequest,
    ) -> Invitation:
        """Invite someone to sign up, and send them the invitation.

        The request is what django-invitations builds the absolute URL of
        the invitation from. Sending is part of the same transaction, so
        that a failure to send does not leave an invitation behind that
        nobody ever received.
        """
        invitation = get_invitation_model().create(email, inviter=inviter)
        invitation.send_invitation(request)
        logger.info("%s invited %s", inviter.email, email)
        return invitation


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
        num_deleted, _ = Subscription.objects.for_user(user).for_comics(comic).delete()
        return num_deleted > 0

    @staticmethod
    @transaction.atomic
    def set_comics(
        *,
        user: ComicsUser,
        comics: Collection[Comic],
    ) -> tuple[list[Comic], list[Comic]]:
        """Subscribe the user to exactly the given comics, and nothing else.

        Returns the comics that were added and the comics that were removed.
        """
        subscribed = list(Comic.objects.subscribed_by(user))
        subscribed_pks = {comic.pk for comic in subscribed}
        wanted_pks = {comic.pk for comic in comics}

        added = [comic for comic in comics if comic.pk not in subscribed_pks]
        removed = [comic for comic in subscribed if comic.pk not in wanted_pks]

        Subscription.objects.for_user(user).for_comics(*removed).delete()
        Subscription.objects.bulk_create(
            [
                Subscription(userprofile=user.comics_profile, comic=comic)
                for comic in added
            ],
            ignore_conflicts=True,
        )

        return added, removed
