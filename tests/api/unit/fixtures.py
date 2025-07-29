import httpx
import pytest
from fastapi.testclient import TestClient

from src.main import fastfitapi


@pytest.fixture(scope="function")
def client() -> httpx.Client:
    with TestClient(fastfitapi) as client:
        yield client
