import json

from django.test.client import Client


def test_openapi_docs_page(db: None, client: Client) -> None:
    response = client.get("/api/v1/docs")

    assert response.status_code == 200
    assert b"swagger" in response.content.lower()


def test_openapi_spec(db: None, client: Client) -> None:
    response = client.get("/api/v1/openapi.json")

    assert response.status_code == 200
    assert b'"/api/v1/comics/"' in response.content
    assert b'"title": "Comics API"' in response.content


def test_openapi_spec_documents_params_and_bodies(db: None, client: Client) -> None:
    response = client.get("/api/v1/openapi.json")

    spec = json.loads(response.content)

    comics_list = spec["paths"]["/api/v1/comics/"]["get"]
    assert comics_list["description"]
    params = {param["name"] for param in comics_list["parameters"]}
    assert params == {
        "limit",
        "offset",
        "subscribed",
        "active",
        "language",
        "name",
        "slug",
    }

    create = spec["paths"]["/api/v1/subscriptions/"]["post"]
    body_schema = create["requestBody"]["content"]["application/json"]["schema"]
    assert body_schema["required"] == ["comic"]


def test_openapi_spec_declares_security_schemes(db: None, client: Client) -> None:
    response = client.get("/api/v1/openapi.json")

    schemes = json.loads(response.content)["components"]["securitySchemes"]
    assert set(schemes) == {"BasicAuth", "SecretKeyBearerAuth"}
    assert schemes["SecretKeyBearerAuth"] == {"type": "http", "scheme": "bearer"}
