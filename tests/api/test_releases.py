import json

from django.test import TestCase
from django.test.client import Client

from . import create_subscriptions, create_user


class ReleasesResourceTestCase(TestCase):
    fixtures = ["comics.json"]

    def setUp(self):
        self.user = create_user()
        self.client = Client()

    def test_requires_authentication(self):
        response = self.client.get("/api/v1/releases/")

        self.assertEqual(response.status_code, 401)

    def test_authentication_with_secret_key_in_header(self):
        response = self.client.get(
            "/api/v1/releases/", headers={"authorization": "Key s3cretk3y"}
        )

        self.assertEqual(response.status_code, 200)

    def test_list_releases(self):
        response = self.client.get(
            "/api/v1/releases/", headers={"authorization": "Key s3cretk3y"}
        )

        data = json.loads(response.content)
        self.assertEqual(len(data["objects"]), 11)

        release = data["objects"][0]
        self.assertEqual(release["comic"], "/api/v1/comics/9/")
        self.assertEqual(release["pub_date"], "2012-10-12")
        self.assertEqual(release["resource_uri"], "/api/v1/releases/11/")
        self.assertEqual(len(release["images"]), 1)

        image = release["images"][0]
        self.assertEqual(image["title"], "Blurring the Line")
        self.assertEqual(
            image["text"],
            "People into masturbatory "
            "navel-gazing have a lot to learn about masturbation.",
        )
        self.assertEqual(image["height"], 235)
        self.assertEqual(image["width"], 740)
        self.assertEqual(
            image["checksum"],
            "76a1407a2730b000d51ccf764c689c8930fdd3580e01f62f70cbe73d8be17e9c",
        )

    def test_subscribed_filter(self):
        create_subscriptions(self.user)

        response = self.client.get(
            "/api/v1/releases/",
            {"subscribed": "true"},
            headers={"authorization": "Key s3cretk3y"},
        )

        data = json.loads(response.content)
        self.assertEqual(len(data["objects"]), 6)

    def test_comic_filter(self):
        response = self.client.get(
            "/api/v1/releases/",
            {"comic__slug": "geekandpoke"},
            headers={"authorization": "Key s3cretk3y"},
        )

        data = json.loads(response.content)
        self.assertEqual(len(data["objects"]), 2)

        release = data["objects"][0]
        self.assertEqual(release["comic"], "/api/v1/comics/4/")

    def test_pub_date_filter(self):
        response = self.client.get(
            "/api/v1/releases/",
            {"pub_date__year": 2012, "pub_date__month": 10},
            headers={"authorization": "Key s3cretk3y"},
        )

        data = json.loads(response.content)
        self.assertEqual(len(data["objects"]), 11)

        response = self.client.get(
            "/api/v1/releases/",
            {"pub_date__year": 2012, "pub_date__month": 9},
            headers={"authorization": "Key s3cretk3y"},
        )

        data = json.loads(response.content)
        self.assertEqual(len(data["objects"]), 0)

    def test_unknown_filter_fails(self):
        response = self.client.get(
            "/api/v1/releases/",
            {"pub_date__foo": "bar"},
            headers={"authorization": "Key s3cretk3y"},
        )

        self.assertEqual(response.status_code, 400)

    def test_details_view(self):
        response = self.client.get(
            "/api/v1/releases/", headers={"authorization": "Key s3cretk3y"}
        )

        data = json.loads(response.content)
        release_uri = data["objects"][0]["resource_uri"]
        self.assertEqual(release_uri, "/api/v1/releases/11/")

        response = self.client.get(
            release_uri, headers={"authorization": "Key s3cretk3y"}
        )

        data = json.loads(response.content)
        self.assertEqual(data["pub_date"], "2012-10-12")
        self.assertEqual(len(data["images"]), 1)
