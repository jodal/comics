from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse


def test_secret_key_page_shows_key_and_links_to_api_docs(
    db: None, client: Client, user: User
) -> None:
    client.force_login(user)

    response = client.get("/me/secret-key/")

    assert response.status_code == 200
    assert b"s3cretk3y" in response.content
    assert b'href="/api/v1/docs"' in response.content


def test_posting_replaces_the_secret_key(db: None, client: Client, user: User) -> None:
    client.force_login(user)

    response = client.post(reverse("secret_key"))

    assert response.status_code == 302

    user.comics_profile.refresh_from_db()
    assert user.comics_profile.secret_key != "s3cretk3y"  # noqa: S105
    assert len(user.comics_profile.secret_key) == 32
