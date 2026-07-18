from django.test.client import Client


def test_openapi_docs_page(db: None, client: Client) -> None:
    response = client.get("/api/v1/docs")

    assert response.status_code == 200
    assert b"swagger" in response.content.lower()


def test_openapi_spec(db: None, client: Client) -> None:
    response = client.get("/api/v1/openapi.json")

    assert response.status_code == 200
    assert b'"/api/v1/comics/"' in response.content
