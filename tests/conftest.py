import pytest
from fastapi.testclient import TestClient

from src.app import App


@pytest.fixture
def app() -> App:
    return App()


@pytest.fixture
def test_client(app: App) -> TestClient:
    return TestClient(app.api)
