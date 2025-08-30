import json

from django.contrib.auth.models import User
from django.test.client import Client


def test_requires_authentication(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/images/")

    assert response.status_code == 401


def test_authentication_with_secret_key_in_header(
    db: None, client: Client, user: User
) -> None:
    response = client.get("/api/v1/images/", headers={"authorization": "Key s3cretk3y"})

    assert response.status_code == 200


def test_lists_images(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/images/", headers={"authorization": "Key s3cretk3y"})

    data = json.loads(response.content)
    assert len(data["objects"]) == 12
    assert data["objects"][0]["height"] == 1132
    assert (
        data["objects"][1]["title"] == "Geek&Poke About The Good Ol' Days In Computers"
    )


def test_height_filter(db: None, client: Client, user: User) -> None:
    response = client.get(
        "/api/v1/images/",
        {"height__gt": 1100},
        headers={"authorization": "Key s3cretk3y"},
    )

    data = json.loads(response.content)
    assert len(data["objects"]) == 2
    assert data["objects"][0]["height"] == 1132
    assert data["objects"][1]["height"] == 1132


def test_details_view(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/images/", headers={"authorization": "Key s3cretk3y"})

    data = json.loads(response.content)
    image_uri = data["objects"][1]["resource_uri"]
    assert image_uri == "/api/v1/images/2/"

    response = client.get(image_uri, headers={"authorization": "Key s3cretk3y"})

    data = json.loads(response.content)
    assert data["title"] == "Geek&Poke About The Good Ol' Days In Computers"
