import pytest

from .fixtures import db_session, db_url  # noqa: F401


def pytest_collection_modifyitems(config, items):
    """
    Automatically mark tests based on filename or other logic.
    Example: mark tests in files with 'schema' in name as 'schema'
    """
    for item in items:
        if "schema" in str(item.fspath):
            item.add_marker(pytest.mark.schema)
        if "endpoint" in str(item.fspath):
            item.add_marker(pytest.mark.endpoint)
        if "crud" in str(item.fspath):
            item.add_marker(pytest.mark.crud)
