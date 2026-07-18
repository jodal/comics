"""Authentication for the API, compatible with the original tastypie setup.

All resources accept the user's secret key, either as an
``Authorization: Key <secret-key>`` header or as a ``?key=`` parameter.
The users resource additionally accepts HTTP basic auth.
"""

from __future__ import annotations

import base64
import binascii
from typing import TYPE_CHECKING

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

if TYPE_CHECKING:
    from django.http import HttpRequest

BASIC_AUTH_REALM = "Comics API"


class SecretKeyAuth:
    def __call__(self, request: HttpRequest) -> User | None:
        secret_key: str | None
        header = request.headers.get("authorization", "")
        if header.lower().startswith("key "):
            parts = header.split()
            if len(parts) != 2:
                return None
            secret_key = parts[1]
        else:
            secret_key = request.GET.get("key")
        if not secret_key:
            return None
        try:
            user = User.objects.get(
                comics_profile__secret_key=secret_key, is_active=True
            )
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
        request.user = user
        return user


class BasicAuth:
    def __call__(self, request: HttpRequest) -> User | None:
        # Mark the request so that a 401 response challenges with basic auth
        request._basic_auth_challenge = True  # type: ignore[attr-defined]

        header = request.headers.get("authorization", "")
        if not header.lower().startswith("basic "):
            return None
        try:
            decoded = base64.b64decode(header.split(" ", 1)[1].strip()).decode()
        except (binascii.Error, UnicodeDecodeError, ValueError):
            return None
        username, _, password = decoded.partition(":")
        user = authenticate(request, username=username, password=password)
        if user is None:
            return None
        request.user = user
        return user
