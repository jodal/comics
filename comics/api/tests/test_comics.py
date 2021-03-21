import json

from django.test import TestCase
from django.test.client import Client

from . import create_subscriptions, create_user


class ComicsResourceTestCase(TestCase):
    fixtures = ["comics.json"]

    def setUp(self):
        self.user = create_user()
        self.client = Client()

    def test_requires_authentication(self):
        response = self.client.get("/api/v1/comics/")

        self.assertEquals(response.status_code, 401)

    def test_authentication_with_secret_key_in_header(self):
        response = self.client.get(
            "/api/v1/comics/", HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        self.assertEquals(response.status_code, 200)

    def test_lists_comics(self):
        response = self.client.get(
            "/api/v1/comics/", HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        data = json.loads(response.content)
        self.assertEquals(len(data["objects"]), 10)
        self.assertEquals(data["objects"][0]["slug"], "abstrusegoose")

    def test_slug_filter(self):
        response = self.client.get(
            "/api/v1/comics/",
            {"slug": "xkcd"},
            HTTP_AUTHORIZATION="Key s3cretk3y",
        )

        data = json.loads(response.content)
        self.assertEquals(len(data["objects"]), 1)
        self.assertEquals(data["objects"][0]["slug"], "xkcd")

    def test_subscribed_filter(self):
        create_subscriptions(self.user)

        response = self.client.get(
            "/api/v1/comics/",
            {"subscribed": "true"},
            HTTP_AUTHORIZATION="Key s3cretk3y",
        )

        data = json.loads(response.content)
        self.assertEquals(len(data["objects"]), 2)
        self.assertEquals(data["objects"][0]["slug"], "geekandpoke")
        self.assertEquals(data["objects"][1]["slug"], "xkcd")

    def test_unsubscribed_filter(self):
        create_subscriptions(self.user)

        response = self.client.get(
            "/api/v1/comics/",
            {"subscribed": "false"},
            HTTP_AUTHORIZATION="Key s3cretk3y",
        )

        data = json.loads(response.content)
        self.assertEquals(len(data["objects"]), 8)
        self.assertEquals(data["objects"][0]["slug"], "abstrusegoose")

    def test_details_view(self):
        response = self.client.get(
            "/api/v1/comics/", HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        data = json.loads(response.content)
        comic_uri = data["objects"][0]["resource_uri"]
        self.assertEquals(comic_uri, "/api/v1/comics/1/")

        response = self.client.get(
            comic_uri, HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        data = json.loads(response.content)
        self.assertEquals(data["slug"], "abstrusegoose")
