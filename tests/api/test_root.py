import json

from django.test.client import Client


def test_get_root_without_authentication(db: None, client: Client) -> None:
    response = client.get("/api/v1/")

    assert response.status_code == 200


def test_root_resource_returns_other_resource_endpoints_in_json(
    db: None, client: Client
) -> None:
    response = client.get("/api/v1/")

    data = json.loads(response.content)
    assert "comics" in data
    assert data["users"]["list_endpoint"] == "/api/v1/users/"
    assert data["comics"]["list_endpoint"] == "/api/v1/comics/"
    assert data["images"]["list_endpoint"] == "/api/v1/images/"
    assert data["releases"]["list_endpoint"] == "/api/v1/releases/"
    assert data["subscriptions"]["list_endpoint"] == "/api/v1/subscriptions/"
