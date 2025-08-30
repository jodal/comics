from typing import cast

import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from pytest_django import DjangoDbBlocker

from comics.accounts.models import Subscription, UserProfile
from comics.core.models import Comic


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup: None, django_db_blocker: DjangoDbBlocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "comics.json")


@pytest.fixture
def subscriptions(user: User) -> list[Subscription]:
    profile = cast("UserProfile", user.comics_profile)  # pyright: ignore[reportAttributeAccessIssue]
    return [
        Subscription.objects.create(
            userprofile=profile,
            comic=Comic.objects.get(slug="geekandpoke"),
        ),
        Subscription.objects.create(
            userprofile=profile,
            comic=Comic.objects.get(slug="xkcd"),
        ),
    ]
