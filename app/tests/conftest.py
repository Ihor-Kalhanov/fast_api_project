import pytest
from fastapi.testclient import TestClient
from app.main import get_app


@pytest.fixture
def test_app():
    app = get_app()
    client = TestClient(app)
    return client
