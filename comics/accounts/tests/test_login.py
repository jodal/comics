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

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/accounts/login/?next=/")

    def test_login_page_includes_email_and_password_fields(self):
        response = self.client.get("/accounts/login/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"E-mail", response.content)
        self.assertIn(b"Password", response.content)

    def test_failed_login_shows_error_on_login_page(self):
        response = self.client.post(
            "/accounts/login/",
            {"login": "alice@example.com", "password": "wrong"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"The e-mail address and/or password you specified are not correct.",
            response.content,
        )
