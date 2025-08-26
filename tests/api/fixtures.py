from contextlib import contextmanager
from datetime import date

import httpx
import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from src import User
from src.api.crud.users import create_user_with_profile, delete_user_db
from src.api.models.enums import FitnessLevelEnum, PrimaryGoalEnum


@pytest.fixture(scope="function")
def db_inspect(db_session: Session):
    return inspect(db_session.bind)


@pytest.fixture(scope="function")
def client(db_url) -> httpx.Client:
    from fastapi.testclient import TestClient

    from src.main import fastfitapi

    with TestClient(fastfitapi) as client:
        yield client


@pytest.fixture
def user_factory(db_session: Session):
    created_users = []

    def _create_user(
        email="example@mail.com",
        password="AWEHiue214@#!",
        birthdate=date(1970, 1, 1),
        height_cm=160,
        weight_kg=60,
        fitness_level=FitnessLevelEnum.beginner.value,
        primary_goal=PrimaryGoalEnum.maintain_health.value,
        delete_all_users=True,
    ):
        if delete_all_users:
            db_session.query(User).delete(synchronize_session=False)
            db_session.commit()

        user, profile = create_user_with_profile(
            db_session,
            email=email,
            password=password,
            birth_date=birthdate,
            height_cm=height_cm,
            weight_kg=weight_kg,
            fitness_level=fitness_level,
            primary_goal=primary_goal,
        )

        created_users.append(user)
        return user, profile

    yield _create_user

    for user in created_users:
        delete_user_db(db_session, user_id=user.user_id)
