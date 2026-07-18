from django.contrib.auth.models import User
from django.test.client import Client


def test_secret_key_page_shows_key_and_links_to_api_docs(
    db: None, client: Client, user: User
) -> None:
    client.force_login(user)

    response = client.get("/me/secret-key/")

    assert response.status_code == 200
    assert b"s3cretk3y" in response.content
    assert b'href="/api/v1/docs"' in response.content
