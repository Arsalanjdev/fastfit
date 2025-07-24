import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import Session


@pytest.fixture(scope="function")
def db_inspect(db_session: Session):
    return inspect(db_session.bind)
