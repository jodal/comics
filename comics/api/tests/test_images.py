import json

from django.test import TestCase
from django.test.client import Client

from . import create_user


class ImagesResourceTestCase(TestCase):
    fixtures = ["comics.json"]

    def setUp(self):
        create_user()
        self.client = Client()

    def test_requires_authentication(self):
        response = self.client.get("/api/v1/images/")

        self.assertEqual(response.status_code, 401)

    def test_authentication_with_secret_key_in_header(self):
        response = self.client.get(
            "/api/v1/images/", HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        self.assertEqual(response.status_code, 200)

    def test_lists_images(self):
        response = self.client.get(
            "/api/v1/images/", HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        data = json.loads(response.content)
        self.assertEqual(len(data["objects"]), 12)
        self.assertEqual(data["objects"][0]["height"], 1132)
        self.assertEqual(
            data["objects"][1]["title"],
            "Geek&Poke About The Good Ol' Days In Computers",
        )

    def test_height_filter(self):
        response = self.client.get(
            "/api/v1/images/",
            {"height__gt": 1100},
            HTTP_AUTHORIZATION="Key s3cretk3y",
        )

        data = json.loads(response.content)
        self.assertEqual(len(data["objects"]), 2)
        self.assertEqual(data["objects"][0]["height"], 1132)
        self.assertEqual(data["objects"][1]["height"], 1132)

    def test_details_view(self):
        response = self.client.get(
            "/api/v1/images/", HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        data = json.loads(response.content)
        image_uri = data["objects"][1]["resource_uri"]
        self.assertEqual(image_uri, "/api/v1/images/2/")

        response = self.client.get(image_uri, HTTP_AUTHORIZATION="Key s3cretk3y")

        data = json.loads(response.content)
        self.assertEqual(
            data["title"], "Geek&Poke About The Good Ol' Days In Computers"
        )
