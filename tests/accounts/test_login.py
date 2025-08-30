from django.contrib.auth.models import User
from django.test.client import Client


def test_front_page_redirects_to_login_page(db: None, client: Client) -> None:
    response = client.get("/")

    assert response.status_code == 302
    assert response["Location"] == "/accounts/login/?next=/"


def test_login_page_includes_email_and_password_fields(
    db: None, client: Client
) -> None:
    response = client.get("/accounts/login/")

    assert response.status_code == 200
    assert b"Email" in response.content
    assert b"Password" in response.content


def test_failed_login_shows_error_on_login_page(
    db: None, client: Client, user: User
) -> None:
    response = client.post(
        "/accounts/login/",
        {"login": "alice@example.com", "password": "wrong"},
    )

    assert response.status_code == 200
    assert (
        b"The email address and/or password you specified are not correct."
        in response.content
    )
