import pytest

from .fixtures import db_session, db_url  # Noqa: F401


def pytest_collection_modifyitems(items):
    for item in items:
        if "schema" in item.name:
            item.add_marker(pytest.mark.schema)
        if "crud" in item.name:
            item.add_marker(pytest.mark.crud)
        if "endpoint" in item.name:
            item.add_marker(pytest.mark.endpoint)
        if "integration" in item.name:
            item.add_marker(pytest.mark.integration)
