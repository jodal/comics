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

        self.assertEqual(response.status_code, 401)

    def test_authentication_with_secret_key_in_header(self):
        response = self.client.get(
            "/api/v1/comics/", headers={"authorization": "Key s3cretk3y"}
        )

        self.assertEqual(response.status_code, 200)

    def test_lists_comics(self):
        response = self.client.get(
            "/api/v1/comics/", headers={"authorization": "Key s3cretk3y"}
        )

        data = json.loads(response.content)
        self.assertEqual(len(data["objects"]), 10)
        self.assertEqual(data["objects"][0]["slug"], "abstrusegoose")

    def test_slug_filter(self):
        response = self.client.get(
            "/api/v1/comics/",
            {"slug": "xkcd"},
            headers={"authorization": "Key s3cretk3y"},
        )

        data = json.loads(response.content)
        self.assertEqual(len(data["objects"]), 1)
        self.assertEqual(data["objects"][0]["slug"], "xkcd")

    def test_subscribed_filter(self):
        create_subscriptions(self.user)

        response = self.client.get(
            "/api/v1/comics/",
            {"subscribed": "true"},
            headers={"authorization": "Key s3cretk3y"},
        )

        data = json.loads(response.content)
        self.assertEqual(len(data["objects"]), 2)
        self.assertEqual(data["objects"][0]["slug"], "geekandpoke")
        self.assertEqual(data["objects"][1]["slug"], "xkcd")

    def test_unsubscribed_filter(self):
        create_subscriptions(self.user)

        response = self.client.get(
            "/api/v1/comics/",
            {"subscribed": "false"},
            headers={"authorization": "Key s3cretk3y"},
        )

        data = json.loads(response.content)
        self.assertEqual(len(data["objects"]), 8)
        self.assertEqual(data["objects"][0]["slug"], "abstrusegoose")

    def test_details_view(self):
        response = self.client.get(
            "/api/v1/comics/", headers={"authorization": "Key s3cretk3y"}
        )

        data = json.loads(response.content)
        comic_uri = data["objects"][0]["resource_uri"]
        self.assertEqual(comic_uri, "/api/v1/comics/1/")

        response = self.client.get(
            comic_uri, headers={"authorization": "Key s3cretk3y"}
        )

        data = json.loads(response.content)
        self.assertEqual(data["slug"], "abstrusegoose")
