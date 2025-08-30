import json

from django.contrib.auth.models import User
from django.test.client import Client

from comics.accounts.models import Subscription


def test_requires_authentication(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/comics/")

    assert response.status_code == 401


def test_authentication_with_secret_key_in_header(
    db: None, client: Client, user: User
) -> None:
    response = client.get("/api/v1/comics/", headers={"authorization": "Key s3cretk3y"})

    assert response.status_code == 200


def test_lists_comics(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/comics/", headers={"authorization": "Key s3cretk3y"})

    data = json.loads(response.content)
    assert len(data["objects"]) == 10
    assert data["objects"][0]["slug"] == "abstrusegoose"


def test_slug_filter(db: None, client: Client, user: User) -> None:
    response = client.get(
        "/api/v1/comics/",
        {"slug": "xkcd"},
        headers={"authorization": "Key s3cretk3y"},
    )

    data = json.loads(response.content)
    assert len(data["objects"]) == 1
    assert data["objects"][0]["slug"] == "xkcd"


def test_subscribed_filter(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    response = client.get(
        "/api/v1/comics/",
        {"subscribed": "true"},
        headers={"authorization": "Key s3cretk3y"},
    )

    data = json.loads(response.content)
    assert len(data["objects"]) == 2
    assert data["objects"][0]["slug"] == "geekandpoke"
    assert data["objects"][1]["slug"] == "xkcd"


def test_unsubscribed_filter(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    response = client.get(
        "/api/v1/comics/",
        {"subscribed": "false"},
        headers={"authorization": "Key s3cretk3y"},
    )

    data = json.loads(response.content)
    assert len(data["objects"]) == 8
    assert data["objects"][0]["slug"] == "abstrusegoose"


def test_details_view(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/comics/", headers={"authorization": "Key s3cretk3y"})

    data = json.loads(response.content)
    comic_uri = data["objects"][0]["resource_uri"]
    assert comic_uri == "/api/v1/comics/1/"

    response = client.get(comic_uri, headers={"authorization": "Key s3cretk3y"})

    data = json.loads(response.content)
    assert data["slug"] == "abstrusegoose"
