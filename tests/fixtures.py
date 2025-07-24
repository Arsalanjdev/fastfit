import os

import pytest
from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def db_url():
    with PostgresContainer("postgres:17") as container:
        url = container.get_connection_url()
        os.environ["TEST_DB_URL"] = url
        alembic_config = Config("alembic.ini")
        alembic_config.set_main_option("sqlalchemy.url", url)
        upgrade(alembic_config, "head")
        yield url


@pytest.fixture()
def db_session(db_url):
    engine = create_engine(db_url)
    session = sessionmaker(bind=engine)
    test_session = session()
    yield test_session
    test_session.rollback()
    test_session.close()
