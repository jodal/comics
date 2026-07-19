"""The comics API, served by django-ninja.

This is a port of the original django-tastypie API. The JSON wire format
-- URLs, envelopes, field names, filtering, and auth -- is kept
compatible with the tastypie implementation, as captured by the test
suite.
"""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any, Protocol, Self, cast

from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404, HttpResponse
from ninja import NinjaAPI
from ninja.errors import AuthenticationError, HttpError

from comics.accounts.models import Subscription
from comics.api.auth import (
    BASIC_AUTH_REALM,
    BasicAuth,
    LegacySecretKeyHeaderAuth,
    LegacySecretKeyQueryAuth,
    SecretKeyBearerAuth,
)
from comics.api.filtering import ALL, FilterSpec, apply_filters
from comics.api.serialization import format_value, json_response, paginated
from comics.core.models import Comic, Image, Release

if TYPE_CHECKING:
    from django.http import HttpRequest

    from comics.accounts.typing import ComicsUser

    class AuthedRequest(HttpRequest):
        auth: ComicsUser


API_PREFIX = "/api/v1"

api = NinjaAPI(title="Comics API", urls_namespace="api")

key_auth = [
    SecretKeyBearerAuth(),
    LegacySecretKeyQueryAuth(),
    LegacySecretKeyHeaderAuth(),
]
users_auth = [BasicAuth(), *key_auth]


# --- Error handling


@api.exception_handler(AuthenticationError)
def on_authentication_error(request: HttpRequest, exc: Exception) -> HttpResponse:
    response = HttpResponse(status=401)
    if getattr(request, "_basic_auth_challenge", False):
        response["WWW-Authenticate"] = f'Basic Realm="{BASIC_AUTH_REALM}"'
    return response


@api.exception_handler(Http404)
def on_not_found(request: HttpRequest, exc: Exception) -> HttpResponse:
    return HttpResponse(status=404)


# --- Serialization


def comic_uri(pk: int) -> str:
    return f"{API_PREFIX}/comics/{pk}/"


def subscription_uri(pk: int) -> str:
    return f"{API_PREFIX}/subscriptions/{pk}/"


def comic_dict(comic: Comic) -> dict[str, Any]:
    return {
        "id": comic.pk,
        "name": comic.name,
        "slug": comic.slug,
        "language": comic.language,
        "url": comic.url,
        "active": comic.active,
        "start_date": format_value(comic.start_date),
        "end_date": format_value(comic.end_date),
        "rights": comic.rights,
        "added": format_value(comic.added),
        "resource_uri": comic_uri(comic.pk),
    }


def image_dict(image: Image) -> dict[str, Any]:
    return {
        "id": image.pk,
        "file": image.file.url if image.file else None,
        "checksum": image.checksum,
        "title": image.title,
        "text": image.text,
        "fetched": format_value(image.fetched),
        "height": image.height,
        "width": image.width,
        "resource_uri": f"{API_PREFIX}/images/{image.pk}/",
    }


def release_dict(release: Release) -> dict[str, Any]:
    return {
        "id": release.pk,
        "comic": comic_uri(release.comic_id),
        "images": [image_dict(image) for image in release.images.all()],
        "pub_date": format_value(release.pub_date),
        "fetched": format_value(release.fetched),
        "resource_uri": f"{API_PREFIX}/releases/{release.pk}/",
    }


def subscription_dict(subscription: Subscription) -> dict[str, Any]:
    return {
        "id": subscription.pk,
        "comic": comic_uri(subscription.comic_id),
        "resource_uri": subscription_uri(subscription.pk),
    }


def user_dict(user: User) -> dict[str, Any]:
    authed_user = cast("ComicsUser", user)
    return {
        "email": authed_user.email,
        "date_joined": format_value(authed_user.date_joined),
        "last_login": format_value(authed_user.last_login),
        "secret_key": authed_user.comics_profile.secret_key,
        "resource_uri": f"{API_PREFIX}/users/{authed_user.pk}/",
    }


# --- Filtering

COMIC_SPEC = FilterSpec(
    model=Comic,
    field_names=frozenset(
        {
            "id",
            "name",
            "slug",
            "language",
            "url",
            "active",
            "start_date",
            "end_date",
            "rights",
            "added",
            "resource_uri",
        }
    ),
    filtering={
        "active": frozenset({"exact"}),
        "language": frozenset({"exact"}),
        "name": ALL,
        "slug": ALL,
    },
)

IMAGE_SPEC = FilterSpec(
    model=Image,
    field_names=frozenset(
        {
            "id",
            "file",
            "checksum",
            "title",
            "text",
            "fetched",
            "height",
            "width",
            "resource_uri",
        }
    ),
    filtering={
        "fetched": ALL,
        "title": ALL,
        "text": ALL,
        "height": ALL,
        "width": ALL,
    },
)

RELEASE_SPEC = FilterSpec(
    model=Release,
    field_names=frozenset(
        {"id", "comic", "images", "pub_date", "fetched", "resource_uri"}
    ),
    filtering={
        "comic": COMIC_SPEC,
        "images": IMAGE_SPEC,
        "pub_date": ALL,
        "fetched": ALL,
    },
)

SUBSCRIPTION_SPEC = FilterSpec(
    model=Subscription,
    field_names=frozenset({"id", "comic", "resource_uri"}),
    filtering={"comic": COMIC_SPEC},
)

USER_SPEC = FilterSpec(
    model=User,
    field_names=frozenset({"email", "date_joined", "last_login", "resource_uri"}),
)


class SubscribableQuerySet(Protocol):
    """A queryset that can be narrowed by a user's subscriptions."""

    def subscribed_by(self, user: User, /) -> Self: ...
    def not_subscribed_by(self, user: User, /) -> Self: ...


def subscribed_filter[QS: SubscribableQuerySet](
    request: AuthedRequest,
    queryset: QS,
) -> QS:
    subscribed = request.GET.get("subscribed")
    if subscribed == "true":
        return queryset.subscribed_by(request.auth)
    if subscribed == "false":
        return queryset.not_subscribed_by(request.auth)
    return queryset


# --- OpenAPI documentation
#
# The responses and the dynamic "field__lookup" filter parameters are
# produced outside django-ninja's schema machinery, so the parameters
# and request bodies are declared in the OpenAPI spec by hand.


def query_param(name: str, description: str, type_: str = "string") -> dict[str, Any]:
    return {
        "in": "query",
        "name": name,
        "required": False,
        "schema": {"type": type_},
        "description": description,
    }


def subscribed_param(noun: str) -> dict[str, Any]:
    return query_param(
        "subscribed",
        f"Only include {noun} the authenticated user is subscribed to "
        "if `true`, or is not subscribed to if `false`.",
        "boolean",
    )


PAGINATION_PARAMS = [
    query_param(
        "limit",
        "Maximum number of objects per response. Defaults to 20, "
        "capped at 1000. Use 0 for the maximum.",
        "integer",
    ),
    query_param("offset", "Offset into the collection. Defaults to 0.", "integer"),
]

COMIC_FILTER_PARAMS = [
    query_param(
        "active",
        "Only include active (`true`) or inactive (`false`) comics.",
        "boolean",
    ),
    query_param("language", "Only include comics in the given language, e.g. `en`."),
    query_param(
        "name",
        "Filter on comic name. Supports Django field lookups, "
        "e.g. `name__startswith=xkcd`.",
    ),
    query_param(
        "slug",
        "Filter on comic slug. Supports Django field lookups, "
        "e.g. `slug__contains=kcd`.",
    ),
]

IMAGE_FILTER_PARAMS = [
    query_param(
        "fetched",
        "Filter on the fetched timestamp. Supports Django field lookups, "
        "e.g. `fetched__gte=2026-01-01T00:00:00+00:00`.",
    ),
    query_param(
        "title",
        "Filter on image title. Supports Django field lookups, "
        "e.g. `title__icontains=cake`.",
    ),
    query_param(
        "text",
        "Filter on image text. Supports Django field lookups, "
        "e.g. `text__icontains=lies`.",
    ),
    query_param(
        "height",
        "Filter on image height. Supports Django field lookups, "
        "e.g. `height__gt=1000`.",
        "integer",
    ),
    query_param(
        "width",
        "Filter on image width. Supports Django field lookups, e.g. `width__gt=1000`.",
        "integer",
    ),
]

RELEASE_FILTER_PARAMS = [
    query_param(
        "comic",
        "Filter on the release's comic, using the comic resource's "
        "filters, e.g. `comic__slug=xkcd`.",
    ),
    query_param(
        "images",
        "Filter on the release's images, using the image resource's "
        "filters, e.g. `images__height__gt=1000`.",
    ),
    query_param(
        "pub_date",
        "Filter on the publication date. Supports Django field lookups, "
        "e.g. `pub_date__year=2026`.",
    ),
    query_param(
        "fetched",
        "Filter on the fetched timestamp. Supports Django field lookups.",
    ),
]

SUBSCRIPTION_FILTER_PARAMS = [
    query_param(
        "comic",
        "Filter on the subscription's comic, using the comic resource's "
        "filters, e.g. `comic__slug=xkcd`.",
    ),
]

SUBSCRIPTION_OBJECT_SCHEMA = {
    "type": "object",
    "properties": {
        "comic": {"type": "string", "example": "/api/v1/comics/1/"},
    },
    "required": ["comic"],
}

SUBSCRIPTION_BODY = {
    "required": True,
    "content": {"application/json": {"schema": SUBSCRIPTION_OBJECT_SCHEMA}},
}

BULK_SUBSCRIPTION_BODY = {
    "required": True,
    "content": {
        "application/json": {
            "schema": {
                "type": "object",
                "properties": {
                    "objects": {
                        "type": "array",
                        "items": SUBSCRIPTION_OBJECT_SCHEMA,
                    },
                    "deleted_objects": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "example": "/api/v1/subscriptions/1/",
                        },
                    },
                },
            },
        },
    },
}


# --- Root resource


@api.get("/")
def root(request: HttpRequest) -> HttpResponse:
    """List the API's resources."""
    resources = ["comics", "images", "releases", "subscriptions", "users"]
    return json_response(
        {name: {"list_endpoint": f"{API_PREFIX}/{name}/"} for name in resources}
    )


# --- Users


@api.get("/users/", auth=users_auth, openapi_extra={"parameters": PAGINATION_PARAMS})
def users_list(request: AuthedRequest) -> HttpResponse:
    """List the authenticated user.

    The result always contains exactly one user: the authenticated one,
    including their secret key. This is the only resource that also
    accepts HTTP basic auth, so it can be used to retrieve the secret
    key given the user's email and password.
    """
    queryset = User.objects.filter(pk=request.auth.pk)
    queryset = apply_filters(request.GET, queryset, USER_SPEC)
    return json_response(paginated(request, queryset, user_dict))


@api.get("/users/{int:user_id}/", auth=users_auth)
def users_detail(request: AuthedRequest, user_id: int) -> HttpResponse:
    """Show a user. Only the authenticated user itself is available."""
    if user_id != request.auth.pk:
        raise Http404
    return json_response(user_dict(request.auth))


# --- Comics


@api.get(
    "/comics/",
    auth=key_auth,
    openapi_extra={
        "parameters": [
            *PAGINATION_PARAMS,
            subscribed_param("comics"),
            *COMIC_FILTER_PARAMS,
        ]
    },
)
def comics_list(request: AuthedRequest) -> HttpResponse:
    """List all comics known to the site."""
    queryset = subscribed_filter(request, Comic.objects.all())
    queryset = apply_filters(request.GET, queryset, COMIC_SPEC)
    return json_response(paginated(request, queryset, comic_dict))


@api.get("/comics/{int:comic_id}/", auth=key_auth)
def comics_detail(request: HttpRequest, comic_id: int) -> HttpResponse:
    """Show a comic."""
    comic = Comic.objects.for_pk(comic_id).get_or_404()
    return json_response(comic_dict(comic))


# --- Images


@api.get(
    "/images/",
    auth=key_auth,
    openapi_extra={"parameters": [*PAGINATION_PARAMS, *IMAGE_FILTER_PARAMS]},
)
def images_list(request: HttpRequest) -> HttpResponse:
    """List comic images.

    You will probably not use this directly, as the images are included
    in full in the releases resource.
    """
    queryset = apply_filters(request.GET, Image.objects.all(), IMAGE_SPEC)
    return json_response(paginated(request, queryset, image_dict))


@api.get("/images/{int:image_id}/", auth=key_auth)
def images_detail(request: HttpRequest, image_id: int) -> HttpResponse:
    """Show a comic image."""
    image = Image.objects.for_pk(image_id).get_or_404()
    return json_response(image_dict(image))


# --- Releases


@api.get(
    "/releases/",
    auth=key_auth,
    openapi_extra={
        "parameters": [
            *PAGINATION_PARAMS,
            subscribed_param("releases"),
            *RELEASE_FILTER_PARAMS,
        ]
    },
)
def releases_list(request: AuthedRequest) -> HttpResponse:
    """List comic releases, most recently fetched first."""
    queryset = (
        Release.objects.select_related("comic")
        .prefetch_related("images")
        .order_by("-fetched")
    )
    queryset = subscribed_filter(request, queryset)
    queryset = apply_filters(request.GET, queryset, RELEASE_SPEC)
    return json_response(paginated(request, queryset, release_dict))


@api.get("/releases/{int:release_id}/", auth=key_auth)
def releases_detail(request: HttpRequest, release_id: int) -> HttpResponse:
    """Show a comic release, including its images."""
    release = Release.objects.select_related("comic").for_pk(release_id).get_or_404()
    return json_response(release_dict(release))


# --- Subscriptions

SUBSCRIPTION_URI_RE = re.compile(rf"^{re.escape(API_PREFIX)}/subscriptions/(\d+)/$")
COMIC_URI_RE = re.compile(rf"^{re.escape(API_PREFIX)}/comics/(\d+)/$")


def parse_body(request: HttpRequest) -> dict[str, Any]:
    try:
        data = json.loads(request.body)
    except ValueError:
        raise HttpError(400, "Request body is not valid JSON") from None
    if not isinstance(data, dict):
        raise HttpError(400, "Request body must be a JSON object")
    return cast("dict[str, Any]", data)


def comic_from_uri(uri: str | None) -> Comic:
    match = COMIC_URI_RE.match(uri or "")
    if match:
        comic = Comic.objects.for_pk(int(match[1])).get_or_none()
        if comic is not None:
            return comic
    raise HttpError(400, f"Unknown comic '{uri}'")


def own_subscription_from_uri(
    request: AuthedRequest,
    uri: str | None,
) -> Subscription | None:
    match = SUBSCRIPTION_URI_RE.match(uri or "")
    if match is None:
        return None
    return (
        Subscription.objects.for_user(request.auth).for_pk(int(match[1])).get_or_none()
    )


@api.get(
    "/subscriptions/",
    auth=key_auth,
    openapi_extra={"parameters": [*PAGINATION_PARAMS, *SUBSCRIPTION_FILTER_PARAMS]},
)
def subscriptions_list(request: AuthedRequest) -> HttpResponse:
    """List the authenticated user's comic subscriptions."""
    queryset = apply_filters(
        request.GET, Subscription.objects.for_user(request.auth), SUBSCRIPTION_SPEC
    )
    return json_response(paginated(request, queryset, subscription_dict))


@api.post(
    "/subscriptions/", auth=key_auth, openapi_extra={"requestBody": SUBSCRIPTION_BODY}
)
def subscriptions_create(request: AuthedRequest) -> HttpResponse:
    """Subscribe the authenticated user to a comic.

    The comic is identified by its resource URI. On success, the new
    subscription's URI is returned in the `Location` header.
    """
    data = parse_body(request)
    comic = comic_from_uri(data.get("comic"))
    subscription = Subscription.objects.create(
        userprofile=request.auth.comics_profile,
        comic=comic,
    )
    response = HttpResponse(status=201)
    response["Location"] = subscription_uri(subscription.pk)
    return response


@api.patch(
    "/subscriptions/",
    auth=key_auth,
    openapi_extra={"requestBody": BULK_SUBSCRIPTION_BODY},
)
@transaction.atomic
def subscriptions_bulk_update(request: AuthedRequest) -> HttpResponse:
    """Create and delete multiple subscriptions in a single request.

    The comics in `objects` are subscribed to, and the subscription URIs
    in `deleted_objects` are unsubscribed from. If any part of the
    update fails, all changes are rolled back.
    """
    data = parse_body(request)
    for obj in data.get("objects", []):
        comic = comic_from_uri(obj.get("comic"))
        if "resource_uri" in obj:
            subscription = own_subscription_from_uri(request, obj["resource_uri"])
            if subscription is None:
                raise Http404
            subscription.comic = comic
            subscription.save()
        else:
            Subscription.objects.create(
                userprofile=request.auth.comics_profile,
                comic=comic,
            )
    for uri in data.get("deleted_objects", []):
        subscription = own_subscription_from_uri(request, uri)
        if subscription is not None:
            subscription.delete()
    return HttpResponse(status=202)


@api.get("/subscriptions/{int:subscription_id}/", auth=key_auth)
def subscriptions_detail(request: AuthedRequest, subscription_id: int) -> HttpResponse:
    """Show one of the authenticated user's subscriptions."""
    subscription = (
        Subscription.objects.for_user(request.auth).for_pk(subscription_id).get_or_404()
    )
    return json_response(subscription_dict(subscription))


@api.put(
    "/subscriptions/{int:subscription_id}/",
    auth=key_auth,
    openapi_extra={"requestBody": SUBSCRIPTION_BODY},
)
def subscriptions_update(request: AuthedRequest, subscription_id: int) -> HttpResponse:
    """Change one of the authenticated user's subscriptions to another comic."""
    subscription = (
        Subscription.objects.for_user(request.auth).for_pk(subscription_id).get_or_404()
    )
    data = parse_body(request)
    subscription.comic = comic_from_uri(data.get("comic"))
    subscription.save()
    return HttpResponse(status=204)


@api.delete("/subscriptions/{int:subscription_id}/", auth=key_auth)
def subscriptions_delete(request: AuthedRequest, subscription_id: int) -> HttpResponse:
    """Unsubscribe the authenticated user from a comic."""
    subscription = (
        Subscription.objects.for_user(request.auth).for_pk(subscription_id).get_or_404()
    )
    subscription.delete()
    return HttpResponse(status=204)
