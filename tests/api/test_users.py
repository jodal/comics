import base64
import json

from django.contrib.auth.models import User
from django.test.client import Client


def test_get_users_without_authentication(db: None, client: Client) -> None:
    response = client.get("/api/v1/users/")

    assert response.status_code == 401


def test_get_users_with_basic_auth(db: None, client: Client, user: User) -> None:
    response = client.get(
        "/api/v1/users/",
        headers={
            "authorization": "Basic {}".format(
                base64.b64encode(b"alice:secret").decode()
            )
        },
    )

    assert response.status_code == 200


def test_get_users_with_secret_key_in_header(
    db: None, client: Client, user: User
) -> None:
    response = client.get("/api/v1/users/", headers={"authorization": "Key s3cretk3y"})

    assert response.status_code == 200


def test_get_users_with_secret_key_in_url(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/users/", {"key": "s3cretk3y"})

    assert response.status_code == 200


def test_response_returns_a_single_user_object(
    db: None, client: Client, user: User
) -> None:
    User.objects.create_user("bob", "bob@example.com", "topsecret")

    response = client.get("/api/v1/users/", headers={"authorization": "Key s3cretk3y"})

    data = json.loads(response.content)
    assert len(data["objects"]) == 1


def test_response_includes_the_secret_key(db: None, client: Client, user: User) -> None:
    response = client.get("/api/v1/users/", headers={"authorization": "Key s3cretk3y"})

    data = json.loads(response.content)
    assert data["objects"][0]["secret_key"] == "s3cretk3y"  # noqa: S105
