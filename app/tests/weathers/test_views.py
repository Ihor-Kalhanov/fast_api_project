from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.asyncio


class TestWeatherView:
    data_from_api = {
        "City": "Lviv",
        "Temperature": 8.92,
        "Feel like": 7.93,
        "Wind speed": 2,
        "Description": "light rain"
    }

    def test_weather_api(self, client: TestClient, city):
        response = client.get(f"/api/weather/{city}/")
        assert response.status_code == status.HTTP_200_OK

    @patch('app.apps.weather.views.get_city', return_value=data_from_api)
    async def test_weather_api_mock(self, get_city):
        response = await get_city('Lviv')

        assert isinstance(response, dict)
        assert response.get('City') == 'Lviv'
        assert response.get('Temperature') == 8.92

    @patch('app.apps.weather.views.get_city', side_effect=Exception('City is not found!'))
    async def test_weather_api_mock_invalid(self, get_city):
        response = await get_city("lviv")
