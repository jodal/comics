import base64
import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from . import create_user


class UsersResourceTestCase(TestCase):
    def setUp(self):
        create_user()
        self.client = Client()

    def test_get_users_without_authentication(self):
        response = self.client.get("/api/v1/users/")

        assert response.status_code == 401

    def test_get_users_with_basic_auth(self):
        response = self.client.get(
            "/api/v1/users/",
            headers={
                "authorization": "Basic {}".format(
                    base64.b64encode(b"alice:secret").decode()
                )
            },
        )

        assert response.status_code == 200

    def test_get_users_with_secret_key_in_header(self):
        response = self.client.get(
            "/api/v1/users/", headers={"authorization": "Key s3cretk3y"}
        )

        assert response.status_code == 200

    def test_get_users_with_secret_key_in_url(self):
        response = self.client.get("/api/v1/users/", {"key": "s3cretk3y"})

        assert response.status_code == 200

    def test_response_returns_a_single_user_object(self):
        User.objects.create_user("bob", "bob@example.com", "topsecret")

        response = self.client.get(
            "/api/v1/users/", headers={"authorization": "Key s3cretk3y"}
        )

        data = json.loads(response.content)
        assert len(data["objects"]) == 1

    def test_response_includes_the_secret_key(self):
        response = self.client.get(
            "/api/v1/users/", headers={"authorization": "Key s3cretk3y"}
        )

        data = json.loads(response.content)
        assert data["objects"][0]["secret_key"] == "s3cretk3y"  # noqa: S105
