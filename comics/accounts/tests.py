from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client


def create_user():
    return User.objects.create_user("alice", "alice@example.com", "secret")


class LoginTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client = Client()

    def test_front_page_redirects_to_login_page(self):
        response = self.client.get("/")

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "/accounts/login/?next=/")

    def test_login_page_includes_email_and_password_fields(self):
        response = self.client.get("/accounts/login/")

        self.assertEquals(response.status_code, 200)
        self.assertIn("Email", response.content)
        self.assertIn("Password", response.content)

    def test_failed_login_shows_error_on_login_page(self):
        response = self.client.post(
            "/accounts/login/",
            {"login": "alice@example.com", "password": "wrong"},
        )

        self.assertEquals(response.status_code, 200)
        self.assertIn(
            "The email address and/or password you "
            "specified are not correct.",
            response.content,
        )
