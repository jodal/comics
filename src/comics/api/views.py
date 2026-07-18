"""The comics API, served by django-ninja.

This is a port of the original django-tastypie API. The JSON wire format
-- URLs, envelopes, field names, filtering, and auth -- is kept
compatible with the tastypie implementation, as captured by the test
suite.
"""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any

from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.errors import AuthenticationError, HttpError

from comics.accounts.models import Subscription
from comics.api.auth import BASIC_AUTH_REALM, BasicAuth, SecretKeyAuth
from comics.api.filtering import ALL, FilterSpec, apply_filters
from comics.api.serialization import format_value, json_response, paginated
from comics.core.models import Comic, Image, Release

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest

    class AuthedRequest(HttpRequest):
        auth: User


API_PREFIX = "/api/v1"

api = NinjaAPI(urls_namespace="api")

key_auth = [SecretKeyAuth()]
users_auth = [BasicAuth(), SecretKeyAuth()]


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
    return {
        "email": user.email,
        "date_joined": format_value(user.date_joined),
        "last_login": format_value(user.last_login),
        "secret_key": user.comics_profile.secret_key,
        "resource_uri": f"{API_PREFIX}/users/{user.pk}/",
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


def subscribed_filter(
    request: AuthedRequest, queryset: QuerySet, lookup: str
) -> QuerySet:
    subscribed = request.GET.get("subscribed")
    if subscribed == "true":
        return queryset.filter(**{lookup: request.auth})
    if subscribed == "false":
        return queryset.exclude(**{lookup: request.auth})
    return queryset


# --- Root resource


@api.get("/")
def root(request: HttpRequest) -> HttpResponse:
    resources = ["comics", "images", "releases", "subscriptions", "users"]
    return json_response(
        {name: {"list_endpoint": f"{API_PREFIX}/{name}/"} for name in resources}
    )


# --- Users


@api.get("/users/", auth=users_auth)
def users_list(request: AuthedRequest) -> HttpResponse:
    queryset = User.objects.filter(pk=request.auth.pk)
    queryset = apply_filters(request.GET, queryset, USER_SPEC)
    return json_response(paginated(request, queryset, user_dict))


@api.get("/users/{int:user_id}/", auth=users_auth)
def users_detail(request: AuthedRequest, user_id: int) -> HttpResponse:
    if user_id != request.auth.pk:
        raise Http404
    return json_response(user_dict(request.auth))


# --- Comics


@api.get("/comics/", auth=key_auth)
def comics_list(request: AuthedRequest) -> HttpResponse:
    queryset = apply_filters(request.GET, Comic.objects.all(), COMIC_SPEC)
    queryset = subscribed_filter(request, queryset, "userprofile__user")
    return json_response(paginated(request, queryset, comic_dict))


@api.get("/comics/{int:comic_id}/", auth=key_auth)
def comics_detail(request: HttpRequest, comic_id: int) -> HttpResponse:
    comic = get_object_or_404(Comic, pk=comic_id)
    return json_response(comic_dict(comic))


# --- Images


@api.get("/images/", auth=key_auth)
def images_list(request: HttpRequest) -> HttpResponse:
    queryset = apply_filters(request.GET, Image.objects.all(), IMAGE_SPEC)
    return json_response(paginated(request, queryset, image_dict))


@api.get("/images/{int:image_id}/", auth=key_auth)
def images_detail(request: HttpRequest, image_id: int) -> HttpResponse:
    image = get_object_or_404(Image, pk=image_id)
    return json_response(image_dict(image))


# --- Releases


@api.get("/releases/", auth=key_auth)
def releases_list(request: AuthedRequest) -> HttpResponse:
    queryset = (
        Release.objects.select_related("comic")
        .prefetch_related("images")
        .order_by("-fetched")
    )
    queryset = apply_filters(request.GET, queryset, RELEASE_SPEC)
    queryset = subscribed_filter(request, queryset, "comic__userprofile__user")
    return json_response(paginated(request, queryset, release_dict))


@api.get("/releases/{int:release_id}/", auth=key_auth)
def releases_detail(request: HttpRequest, release_id: int) -> HttpResponse:
    release = get_object_or_404(Release.objects.select_related("comic"), pk=release_id)
    return json_response(release_dict(release))


# --- Subscriptions

SUBSCRIPTION_URI_RE = re.compile(rf"^{re.escape(API_PREFIX)}/subscriptions/(\d+)/$")
COMIC_URI_RE = re.compile(rf"^{re.escape(API_PREFIX)}/comics/(\d+)/$")


def own_subscriptions(request: AuthedRequest) -> QuerySet[Subscription]:
    return Subscription.objects.filter(userprofile__user=request.auth)


def parse_body(request: HttpRequest) -> dict[str, Any]:
    try:
        data = json.loads(request.body)
    except ValueError:
        raise HttpError(400, "Request body is not valid JSON") from None
    if not isinstance(data, dict):
        raise HttpError(400, "Request body must be a JSON object")
    return data


def comic_from_uri(uri: str | None) -> Comic:
    match = COMIC_URI_RE.match(uri or "")
    if match:
        try:
            return Comic.objects.get(pk=int(match[1]))
        except Comic.DoesNotExist:
            pass
    raise HttpError(400, f"Unknown comic '{uri}'")


def own_subscription_from_uri(
    request: AuthedRequest, uri: str | None
) -> Subscription | None:
    match = SUBSCRIPTION_URI_RE.match(uri or "")
    if match is None:
        return None
    return own_subscriptions(request).filter(pk=int(match[1])).first()


@api.get("/subscriptions/", auth=key_auth)
def subscriptions_list(request: AuthedRequest) -> HttpResponse:
    queryset = apply_filters(request.GET, own_subscriptions(request), SUBSCRIPTION_SPEC)
    return json_response(paginated(request, queryset, subscription_dict))


@api.post("/subscriptions/", auth=key_auth)
def subscriptions_create(request: AuthedRequest) -> HttpResponse:
    data = parse_body(request)
    comic = comic_from_uri(data.get("comic"))
    subscription = Subscription.objects.create(
        userprofile=request.auth.comics_profile,
        comic=comic,
    )
    response = HttpResponse(status=201)
    response["Location"] = subscription_uri(subscription.pk)
    return response


@api.patch("/subscriptions/", auth=key_auth)
@transaction.atomic
def subscriptions_bulk_update(request: AuthedRequest) -> HttpResponse:
    data = parse_body(request)
    for obj in data.get("objects", []):
        comic = comic_from_uri(obj.get("comic"))
        if "resource_uri" in obj:
            subscription = own_subscription_from_uri(request, obj["resource_uri"])
            if subscription is None:
                raise Http404
            subscription.comic_id = comic.pk
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
    subscription = get_object_or_404(own_subscriptions(request), pk=subscription_id)
    return json_response(subscription_dict(subscription))


@api.put("/subscriptions/{int:subscription_id}/", auth=key_auth)
def subscriptions_update(request: AuthedRequest, subscription_id: int) -> HttpResponse:
    subscription = get_object_or_404(own_subscriptions(request), pk=subscription_id)
    data = parse_body(request)
    subscription.comic_id = comic_from_uri(data.get("comic")).pk
    subscription.save()
    return HttpResponse(status=204)


@api.delete("/subscriptions/{int:subscription_id}/", auth=key_auth)
def subscriptions_delete(request: AuthedRequest, subscription_id: int) -> HttpResponse:
    subscription = get_object_or_404(own_subscriptions(request), pk=subscription_id)
    subscription.delete()
    return HttpResponse(status=204)
