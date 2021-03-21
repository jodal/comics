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

        self.assertEquals(response.status_code, 401)

    def test_get_users_with_basic_auth(self):
        response = self.client.get(
            "/api/v1/users/",
            HTTP_AUTHORIZATION="Basic %s" % base64.encodestring("alice:secret"),
        )

        self.assertEquals(response.status_code, 200)

    def test_get_users_with_secret_key_in_header(self):
        response = self.client.get(
            "/api/v1/users/", HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        self.assertEquals(response.status_code, 200)

    def test_get_users_with_secret_key_in_url(self):
        response = self.client.get("/api/v1/users/", {"key": "s3cretk3y"})

        self.assertEquals(response.status_code, 200)

    def test_response_returns_a_single_user_object(self):
        User.objects.create_user("bob", "bob@example.com", "topsecret")

        response = self.client.get(
            "/api/v1/users/", HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        data = json.loads(response.content)
        self.assertEquals(len(data["objects"]), 1)

    def test_response_includes_the_secret_key(self):
        response = self.client.get(
            "/api/v1/users/", HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        data = json.loads(response.content)
        self.assertEquals(data["objects"][0]["secret_key"], "s3cretk3y")
