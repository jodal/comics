"""Tests pinning wire-format details preserved from the original tastypie API.

The API was ported from django-tastypie to django-ninja with a
compatible JSON wire format. These tests cover the compatibility details
that are easy to get wrong and that the resource-focused tests don't
cover: serialization formats, the list envelope, pagination, filter
validation, and error responses.
"""

import json

from django.contrib.auth.models import User
from django.test.client import Client

from comics.core.models import Comic

KEY_AUTH = {"authorization": "Key s3cretk3y"}


# --- Serialization


def test_datetimes_are_naive_iso_8601_with_microseconds(
    db: None, client: Client, user: User
) -> None:
    response = client.get("/api/v1/comics/1/", headers=KEY_AUTH)

    data = json.loads(response.content)
    assert data["added"] == "2012-10-12T23:09:08.251000"


def test_comic_objects_have_all_model_fields(
    db: None, client: Client, user: User
) -> None:
    response = client.get("/api/v1/comics/1/", headers=KEY_AUTH)

    data = json.loads(response.content)
    assert set(data) == {
        "active",
        "added",
        "end_date",
        "id",
        "language",
        "name",
        "resource_uri",
        "rights",
        "slug",
        "start_date",
        "url",
    }


def test_release_objects_have_full_image_objects(
    db: None, client: Client, user: User
) -> None:
    response = client.get("/api/v1/releases/11/", headers=KEY_AUTH)

    data = json.loads(response.content)
    assert set(data) == {
        "comic",
        "fetched",
        "id",
        "images",
        "pub_date",
        "resource_uri",
    }
    assert set(data["images"][0]) == {
        "checksum",
        "fetched",
        "file",
        "height",
        "id",
        "resource_uri",
        "text",
        "title",
        "width",
    }


def test_image_file_is_a_media_url_path(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/images/1/", headers=KEY_AUTH)

    data = json.loads(response.content)
    assert data["file"].startswith("/media/")
    assert data["file"].endswith(".jpg")


def test_user_objects_have_no_id_field(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/users/", headers=KEY_AUTH)

    data = json.loads(response.content)
    assert set(data["objects"][0]) == {
        "date_joined",
        "email",
        "last_login",
        "resource_uri",
        "secret_key",
    }


def test_responses_are_json_without_charset_parameter(
    db: None, client: Client, user: User
) -> None:
    response = client.get("/api/v1/comics/", headers=KEY_AUTH)

    assert response.headers["Content-Type"] == "application/json"


def test_legacy_format_and_callback_params_are_ignored(
    db: None, client: Client, user: User
) -> None:
    response = client.get(
        "/api/v1/comics/",
        {"format": "xml", "callback": "foo"},
        headers=KEY_AUTH,
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    data = json.loads(response.content)
    assert data["meta"]["total_count"] == 10


# --- Pagination


def test_list_envelope_has_meta_and_objects(
    db: None, client: Client, user: User
) -> None:
    response = client.get("/api/v1/comics/", headers=KEY_AUTH)

    data = json.loads(response.content)
    assert set(data) == {"meta", "objects"}
    assert data["meta"] == {
        "limit": 20,
        "next": None,
        "offset": 0,
        "previous": None,
        "total_count": 10,
    }


def test_pagination_links_preserve_query_params(
    db: None, client: Client, user: User
) -> None:
    response = client.get(
        "/api/v1/comics/",
        {"slug__contains": "a", "limit": "3", "offset": "3"},
        headers=KEY_AUTH,
    )

    meta = json.loads(response.content)["meta"]
    assert meta["limit"] == 3
    assert meta["offset"] == 3
    assert meta["next"] == "/api/v1/comics/?slug__contains=a&limit=3&offset=6"
    assert meta["previous"] == "/api/v1/comics/?slug__contains=a&limit=3&offset=0"


def test_limit_zero_means_max_limit(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/comics/", {"limit": "0"}, headers=KEY_AUTH)

    data = json.loads(response.content)
    assert data["meta"]["limit"] == 1000
    assert len(data["objects"]) == 10


def test_non_integer_limit_returns_400(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/comics/", {"limit": "x"}, headers=KEY_AUTH)

    assert response.status_code == 400
    assert json.loads(response.content) == {
        "error": "Invalid limit 'x' provided. Please provide a positive integer."
    }


def test_negative_offset_returns_400(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/comics/", {"offset": "-1"}, headers=KEY_AUTH)

    assert response.status_code == 400
    assert json.loads(response.content) == {
        "error": "Invalid offset '-1' provided. Please provide a positive integer >= 0."
    }


# --- Filtering


def test_unknown_params_are_silently_ignored(
    db: None, client: Client, user: User
) -> None:
    response = client.get("/api/v1/comics/", {"foobar": "baz"}, headers=KEY_AUTH)

    data = json.loads(response.content)
    assert data["meta"]["total_count"] == 10


def test_unfilterable_field_returns_400(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/comics/", {"rights": "foo"}, headers=KEY_AUTH)

    assert response.status_code == 400
    assert json.loads(response.content) == {
        "error": "The 'rights' field does not allow filtering."
    }


def test_invalid_lookup_returns_400(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/comics/", {"slug__foo": "bar"}, headers=KEY_AUTH)

    assert response.status_code == 400
    assert json.loads(response.content) == {
        "error": "The 'slug' field does not support relations."
    }


def test_disallowed_lookup_returns_400(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/comics/", {"active__gt": "true"}, headers=KEY_AUTH)

    assert response.status_code == 400
    assert json.loads(response.content) == {
        "error": "'gt' is not an allowed filter on the 'active' field."
    }


def test_boolean_filter_values_are_converted(
    db: None, client: Client, user: User
) -> None:
    expected = Comic.objects.filter(active=False).count()
    assert expected > 0

    response = client.get("/api/v1/comics/", {"active": "false"}, headers=KEY_AUTH)

    data = json.loads(response.content)
    assert data["meta"]["total_count"] == expected


def test_in_lookup_accepts_comma_separated_values(
    db: None, client: Client, user: User
) -> None:
    response = client.get(
        "/api/v1/comics/", {"slug__in": "xkcd,bunny"}, headers=KEY_AUTH
    )

    data = json.loads(response.content)
    assert {obj["slug"] for obj in data["objects"]} == {"bunny", "xkcd"}


# --- Authentication and error responses


def test_401_has_empty_body(db: None, client: Client) -> None:
    response = client.get("/api/v1/comics/")

    assert response.status_code == 401
    assert response.content == b""
    assert "WWW-Authenticate" not in response.headers


def test_users_401_challenges_with_basic_auth(db: None, client: Client) -> None:
    response = client.get("/api/v1/users/")

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == 'Basic Realm="Comics API"'


def test_wrong_key_returns_401(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/comics/", headers={"authorization": "Key wrong"})

    assert response.status_code == 401


def test_malformed_key_header_returns_401(db: None, client: Client, user: User) -> None:
    response = client.get(
        "/api/v1/comics/", headers={"authorization": "Key s3cret k3y"}
    )

    assert response.status_code == 401


def test_missing_object_returns_empty_404(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/comics/666/", headers=KEY_AUTH)

    assert response.status_code == 404
    assert response.content == b""

