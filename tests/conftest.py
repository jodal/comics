from collections.abc import Generator
from typing import TYPE_CHECKING, cast

import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import override_settings

if TYPE_CHECKING:
    from comics.accounts.models import UserProfile


@pytest.fixture(scope="session", autouse=True)
def staticfiles(tmp_path_factory):
    with override_settings(
        STATIC_ROOT=tmp_path_factory.mktemp("static"),
        COMPRESS_ENABLED=False,
    ):
        call_command("collectstatic", "--noinput")
        yield


@pytest.fixture
def user() -> User:
    user = User.objects.create_user("alice", "alice@example.com", "secret")
    profile = cast("UserProfile", user.comics_profile)  # pyright: ignore[reportAttributeAccessIssue]
    profile.secret_key = "s3cretk3y"  # noqa: S105
    profile.save()
    return user
