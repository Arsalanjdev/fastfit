from sqlalchemy import text

# from .fixtures import db_session


def test_dummy(db_session):
    """Check that we can connect to the database."""
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1
