import pytest

from fastapi.testclient import TestClient
from app.main import get_app


@pytest.fixture
def test_app():
    client = TestClient(get_app())
    yield client
