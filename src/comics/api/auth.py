"""Authentication for the API.

All resources accept the user's secret key as a standard bearer token
in the ``Authorization`` header. The users resource additionally
accepts HTTP basic auth.

The advertised auth classes extend django-ninja's security classes, so
that the OpenAPI spec declares the security schemes and the interactive
API docs offer to authenticate requests.

Two unadvertised ways of providing the secret key are also accepted,
for old clients: the tastypie-era ``Authorization: Key <secret-key>``
header and the ``?key=`` query parameter. They are plain callables
rather than django-ninja security classes, keeping them out of the
OpenAPI spec, to steer clients towards the ``Authorization`` header
and keep secret keys out of URLs, caches, and server logs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ninja.security import HttpBasicAuth, HttpBearer

if TYPE_CHECKING:
    from django.http import HttpRequest

BASIC_AUTH_REALM = "Comics API"


def _user_from_secret_key(request: HttpRequest, secret_key: str | None) -> User | None:
    if not secret_key:
        return None
    try:
        user = User.objects.get(comics_profile__secret_key=secret_key, is_active=True)
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        return None
    request.user = user
    return user


class SecretKeyBearerAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> User | None:
        return _user_from_secret_key(request, token)


class LegacySecretKeyQueryAuth:
    """The ``?key=<secret-key>`` query parameter."""

    def __call__(self, request: HttpRequest) -> User | None:
        return _user_from_secret_key(request, request.GET.get("key"))


class LegacySecretKeyHeaderAuth:
    """The tastypie-era ``Authorization: Key <secret-key>`` header.

    A plain callable rather than a django-ninja security class, so that
    it is not declared in the OpenAPI spec.
    """

    def __call__(self, request: HttpRequest) -> User | None:
        parts = request.headers.get("Authorization", "").split()
        if len(parts) != 2 or parts[0].lower() != "key":
            return None
        return _user_from_secret_key(request, parts[1])


class BasicAuth(HttpBasicAuth):
    def __call__(self, request: HttpRequest) -> User | None:
        # Mark the request so that a 401 response challenges with basic auth
        request._basic_auth_challenge = True  # type: ignore[attr-defined]
        return super().__call__(request)

    def authenticate(
        self, request: HttpRequest, username: str, password: str
    ) -> User | None:
        user = authenticate(request, username=username, password=password)
        if user is None:
            return None
        request.user = user
        return user  # type: ignore[return-value]
