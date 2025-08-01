import httpx
import pytest


@pytest.fixture(scope="function")
def client(db_url) -> httpx.Client:
    from fastapi.testclient import TestClient

    from src.main import fastfitapi

    with TestClient(fastfitapi) as client:
        yield client
