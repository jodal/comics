import json

from django.test import TestCase
from django.test.client import Client


class RootResourceTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_root_without_authentication(self):
        response = self.client.get("/api/v1/")

        self.assertEquals(response.status_code, 200)

    def test_root_resource_returns_other_resource_endpoints_in_json(self):
        response = self.client.get("/api/v1/")

        data = json.loads(response.content)
        self.assertIn("comics", data)
        self.assertEquals(data["users"]["list_endpoint"], "/api/v1/users/")
        self.assertEquals(data["comics"]["list_endpoint"], "/api/v1/comics/")
        self.assertEquals(data["images"]["list_endpoint"], "/api/v1/images/")
        self.assertEquals(data["releases"]["list_endpoint"], "/api/v1/releases/")
        self.assertEquals(
            data["subscriptions"]["list_endpoint"], "/api/v1/subscriptions/"
        )

    def test_resource_can_return_xml(self):
        response = self.client.get("/api/v1/", HTTP_ACCEPT="application/xml")

        self.assertIn("<?xml version='1.0' encoding='utf-8'?>", response.content)

    def test_resource_can_return_jsonp(self):
        response = self.client.get("/api/v1/", {"format": "jsonp"})

        self.assertIn("callback(", response.content)

    def test_resource_can_return_jsonp_with_custom_callback_name(self):
        response = self.client.get("/api/v1/", {"format": "jsonp", "callback": "foo"})

        self.assertIn("foo(", response.content)

    def test_resource_returns_jsonp_if_just_given_callback_name(self):
        response = self.client.get("/api/v1/", {"callback": "foo"})

        self.assertIn("foo(", response.content)
