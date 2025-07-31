"""
Tests for crud operations on db
"""

from datetime import datetime
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from src.api.crud.users import (
    create_user_db,
    create_user_with_profile,
    delete_user_db,
    get_user_by_email,
    get_user_by_id,
)
from tests.utils import is_iso_datetime, is_valid_uuid

# @contextmanager
# def temporary_user(db_session: Session, email:str="email@example.com", password:str="12345") -> User:
#     uuid = uuid4()
#     created_at = datetime.now().isoformat()
#
#     user = User(
#         user_id=uuid,
#         email=email,
#         created_at=created_at,
#         is_active=True,
#         password=password,
#         role="user",
#     )
#
#     db_session.add(user)
#     db_session.commit()
#     db_session.refresh(user)
#
#     try:
#         yield user
#     finally:
#         db_session.delete(user)
#         db_session.commit()


def test_crud_user_create(db_session):
    email = "example@mail.com"
    password = "12345"
    user = create_user_db(db_session, email, password)
    assert user.email == email
    assert user.password == password
    assert user.role == "user"
    assert is_iso_datetime(user.created_at.isoformat())
    assert is_valid_uuid(str(user.user_id))
    assert user.is_active
    db_session.delete(user)
    db_session.commit()


def test_crud_create_user_with_profile(db_session):
    email = "example@mail.com"
    password = "12345"
    birthdate = datetime.now().isoformat()
    user = create_user_db(db_session, email, password)
    user, profile = create_user_with_profile(
        db=db_session,
        email=email,
        password=password,
        birth_date=birthdate,
        height_cm=120.34,
        weight_kg=80.74,
    )


def test_crud_user_create_duplicated_email(db_session):
    email = "email@example.com"
    password = "12345"
    user = create_user_db(db_session, email, password)
    db_session.commit()
    db_session.refresh(user)
    with pytest.raises(IntegrityError):
        create_user_db(db_session, email, password)
        db_session.flush()
    db_session.rollback()
    db_session.delete(user)
    db_session.commit()


def test_crud_user_get_user_by_email(db_session):
    email = "user@example.com"
    password = "securepassword"

    user_created = create_user_db(db_session, email=email, password=password)
    db_session.commit()

    user_fetched = get_user_by_email(db_session, email)

    assert user_fetched is not None
    assert user_fetched.email == email
    assert user_fetched.user_id == user_created.user_id

    user_none = get_user_by_email(db_session, "notfound@example.com")
    assert user_none is None

    db_session.delete(user_created)
    db_session.commit()


def test_crud_user_get_user_by_id(db_session):
    email = "user@example.com"
    password = "securepassword"

    user_created = create_user_db(db_session, email=email, password=password)
    db_session.commit()

    user_fetched = get_user_by_id(db_session, user_created.user_id)

    assert user_fetched is not None
    assert user_fetched.email == email
    assert user_fetched.user_id == user_created.user_id

    user_none = get_user_by_id(db_session, user_id=uuid4())
    assert user_none is None
    db_session.delete(user_created)
    db_session.commit()


def test_crud_user_update_email(db_session):
    email = "email@example.com"
    password = "12345"
    user = create_user_db(db_session, email, password)
    db_session.commit()
    db_session.refresh(user)
    user.email = "email2@example.com"
    db_session.commit()
    db_session.refresh(user)
    assert user.email == "email2@example.com"
    assert user.email != "email@example.com"
    db_session.delete(user)
    db_session.commit()


def test_crud_user_deletion(db_session):
    email = "email@example.com"
    password = "12345"
    user = create_user_db(db_session, email, password)
    db_session.commit()
    db_session.refresh(user)
    is_deleted = delete_user_db(db_session, user_id=user.user_id)
    assert is_deleted
    assert get_user_by_id(db_session, user_id=user.user_id) is None


def test_crud_user_deletion_non_existent_user(db_session):
    email = "email@example.com"
    password = "12345"
    user = create_user_db(db_session, email, password)
    db_session.commit()
    db_session.refresh(user)
    delete_user_db(db_session, user_id=user.user_id)
    second_time = delete_user_db(db_session, user_id=user.user_id)
    assert second_time is False
