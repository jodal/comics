import json

import pytest
from django.contrib.auth.models import User
from django.test.client import Client

from comics.accounts.models import Subscription
from comics.core.models import Comic


def test_requires_authentication(db: None, client: Client) -> None:
    response = client.get("/api/v1/subscriptions/")

    assert response.status_code == 401


def test_authentication_with_secret_key_in_header(
    db: None,
    client: Client,
    user: User,
) -> None:
    response = client.get(
        "/api/v1/subscriptions/", headers={"authorization": "Key s3cretk3y"}
    )

    assert response.status_code == 200


def test_list_subscriptions(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    subscription = Subscription.objects.all()[0]

    response = client.get(
        "/api/v1/subscriptions/", headers={"authorization": "Key s3cretk3y"}
    )

    data = json.loads(response.content)
    assert len(data["objects"]) == 2

    sub = data["objects"][0]
    assert sub["resource_uri"] == ("/api/v1/subscriptions/%d/" % subscription.pk)
    assert sub["comic"] == ("/api/v1/comics/%d/" % subscription.comic.pk)


def test_comic_filter(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    subscription = Subscription.objects.get(comic__slug="xkcd")

    response = client.get(
        "/api/v1/subscriptions/",
        {"comic__slug": "xkcd"},
        headers={"authorization": "Key s3cretk3y"},
    )

    data = json.loads(response.content)
    assert len(data["objects"]) == 1

    sub = data["objects"][0]
    assert sub["resource_uri"] == ("/api/v1/subscriptions/%d/" % subscription.pk)
    assert sub["comic"] == "/api/v1/comics/9/"


def test_details_view(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    subscription = Subscription.objects.all()[0]

    response = client.get(
        "/api/v1/subscriptions/", headers={"authorization": "Key s3cretk3y"}
    )

    data = json.loads(response.content)
    sub = data["objects"][0]
    assert sub["resource_uri"] == ("/api/v1/subscriptions/%d/" % subscription.pk)

    response = client.get(
        sub["resource_uri"], headers={"authorization": "Key s3cretk3y"}
    )

    data = json.loads(response.content)
    assert data["comic"] == ("/api/v1/comics/%d/" % subscription.comic.pk)


def test_subscribe_to_comic(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    comic = Comic.objects.get(slug="bunny")

    data = json.dumps({"comic": "/api/v1/comics/%d/" % comic.pk})
    response = client.post(
        "/api/v1/subscriptions/",
        data=data,
        content_type="application/json",
        headers={"authorization": "Key s3cretk3y"},
    )

    assert response.status_code == 201

    subscription = Subscription.objects.get(userprofile__user=user, comic=comic)
    assert response["Location"] == ("/api/v1/subscriptions/%d/" % subscription.pk)

    assert response.content == b""


def test_unsubscribe_from_comic(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    sub = Subscription.objects.get(comic__slug="xkcd")

    assert Subscription.objects.filter(userprofile__user=user).count() == 2

    response = client.delete(
        "/api/v1/subscriptions/%d/" % sub.pk,
        headers={"authorization": "Key s3cretk3y"},
    )

    assert response.status_code == 204
    assert response.content == b""

    assert Subscription.objects.filter(userprofile__user=user).count() == 1


@pytest.mark.skip(reason="Django test client doesn't support PATCH yet")
def test_bulk_update() -> None:
    # XXX: "PATCH /api/v1/subscriptions/" isn't tested as Django's test
    # client doesn't support the PATCH method yet. See
    # https://code.djangoproject.com/ticket/17797 to check if PATCH support
    # has been added yet.
    pass
