from fastapi import status
from fastapi.testclient import TestClient

from app.tests.conftest import car_data


class TestViewsCar:

    def test_list_cars(self, client: TestClient, catalog):
        response = client.get(f'/api/catalog/{catalog.id}/cars/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["cars"]) == 0

    def test_get_one_car(self, client: TestClient, car):
        response = client.get(f'/api/catalog/{car.id}')
        assert response.status_code == status.HTTP_200_OK

    def test_get_one_car_not_exist(self, client: TestClient, ):
        response = client.get(f'/api/catalog/0/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_car(self, client: TestClient, catalog):
        response = client.post(
            f'/api/catalog/{catalog.id}/cars/',
            json=[car_data.dict()]
        )

        assert response.status_code == status.HTTP_200_OK

    def test_update_car(self, client: TestClient, catalog, car):
        response = client.put(
            f'/api/catalog/{catalog.id}/cars/',
            json={
                "id": car.id,
                "name": "updated name",
                "description": "updated description"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['name'] == 'updated name'
        assert response.json()['description'] == 'updated description'

