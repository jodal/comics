from __future__ import annotations

from typing import Any

from django.contrib.auth.models import User
from django.db import models

from comics.accounts.services import UserProfileService


def connect() -> None:
    """Connect the receivers below. Called from `AccountsConfig.ready()`."""
    models.signals.post_save.connect(create_user_profile, sender=User)


def create_user_profile(
    sender: type[User],
    instance: User,
    created: bool,
    **kwargs: Any,
) -> None:
    if created:
        UserProfileService.create_for_user(user=instance)
