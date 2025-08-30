import json

from django.test import TestCase
from django.test.client import Client


class RootResourceTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_root_without_authentication(self):
        response = self.client.get("/api/v1/")

        assert response.status_code == 200

    def test_root_resource_returns_other_resource_endpoints_in_json(self):
        response = self.client.get("/api/v1/")

        data = json.loads(response.content)
        assert "comics" in data
        assert data["users"]["list_endpoint"] == "/api/v1/users/"
        assert data["comics"]["list_endpoint"] == "/api/v1/comics/"
        assert data["images"]["list_endpoint"] == "/api/v1/images/"
        assert data["releases"]["list_endpoint"] == "/api/v1/releases/"
        assert data["subscriptions"]["list_endpoint"] == "/api/v1/subscriptions/"

    def test_resource_can_return_xml(self):
        response = self.client.get("/api/v1/", headers={"accept": "application/xml"})

        assert b"<?xml version='1.0' encoding='utf-8'?>" in response.content

    def test_resource_can_return_jsonp(self):
        response = self.client.get("/api/v1/", {"format": "jsonp"})

        assert b"callback(" in response.content

    def test_resource_can_return_jsonp_with_custom_callback_name(self):
        response = self.client.get("/api/v1/", {"format": "jsonp", "callback": "foo"})

        assert b"foo(" in response.content

    def test_resource_returns_jsonp_if_just_given_callback_name(self):
        response = self.client.get("/api/v1/", {"callback": "foo"})

        assert b"foo(" in response.content
