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

        assert response.status_code == 401

    def test_authentication_with_secret_key_in_header(self):
        response = self.client.get(
            "/api/v1/images/", headers={"authorization": "Key s3cretk3y"}
        )

        assert response.status_code == 200

    def test_lists_images(self):
        response = self.client.get(
            "/api/v1/images/", headers={"authorization": "Key s3cretk3y"}
        )

        data = json.loads(response.content)
        assert len(data["objects"]) == 12
        assert data["objects"][0]["height"] == 1132
        assert (
            data["objects"][1]["title"]
            == "Geek&Poke About The Good Ol' Days In Computers"
        )

    def test_height_filter(self):
        response = self.client.get(
            "/api/v1/images/",
            {"height__gt": 1100},
            headers={"authorization": "Key s3cretk3y"},
        )

        data = json.loads(response.content)
        assert len(data["objects"]) == 2
        assert data["objects"][0]["height"] == 1132
        assert data["objects"][1]["height"] == 1132

    def test_details_view(self):
        response = self.client.get(
            "/api/v1/images/", headers={"authorization": "Key s3cretk3y"}
        )

        data = json.loads(response.content)
        image_uri = data["objects"][1]["resource_uri"]
        assert image_uri == "/api/v1/images/2/"

        response = self.client.get(
            image_uri, headers={"authorization": "Key s3cretk3y"}
        )

        data = json.loads(response.content)
        assert data["title"] == "Geek&Poke About The Good Ol' Days In Computers"
