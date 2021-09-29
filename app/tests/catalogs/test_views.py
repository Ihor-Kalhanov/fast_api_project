from fastapi import status
from fastapi.testclient import TestClient


class TestViewsCatalog:

    def test_get_catalogs_empty(self, client: TestClient):
        response = client.get("/api/catalog/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["catalogs"]) == 0

    def test_get_catalogs_not_exist(self, client: TestClient):
        response = client.get("/api/catalog/0/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_catalog(self, client: TestClient):
        response = client.post(
            "/api/catalog/",
            json={
                "title": "test_post_catalog_title"
            }
        )
        assert response.status_code == status.HTTP_200_OK

    def test_create_catalog_not_exist(self, client: TestClient, catalog):
        response = client.post(
            "/api/catalog/",
            json={
                "title": catalog.title,
                "id": catalog.id
            }
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_update_catalog(self, client: TestClient, catalog):
        response = client.put(
            f"/api/catalog/{catalog.id}/",
            json={
                "title": "test_post_catalog_title_updated"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['title'] == 'test_post_catalog_title_updated'
