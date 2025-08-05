import httpx
import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import Session


@pytest.fixture(scope="function")
def db_inspect(db_session: Session):
    return inspect(db_session.bind)


@pytest.fixture(scope="function")
def client(db_url) -> httpx.Client:
    from fastapi.testclient import TestClient

    from src.main import fastfitapi

    with TestClient(fastfitapi) as client:
        yield client
