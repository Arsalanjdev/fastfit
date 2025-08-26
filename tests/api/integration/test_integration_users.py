from datetime import date

import pytest
from fastapi import HTTPException

from src.api.crud.users import delete_user_db
from src.api.models.enums import FitnessLevelEnum, GenderEnum, PrimaryGoalEnum


def test_integration_users_signup_duplicated_email(db_session, client):
    """
    Tests the endpoint rejects the duplicate email sign up.
    :param client:
    :return:
    """
    # signing up the first user
    email = "ema313il@example.com"
    password = "!AWEHwioe41j250!"
    user = {
        "email": email,
        "password": password,
    }
    profile = {
        "birth_date": date(1980, 2, 3).isoformat(),
        "gender": GenderEnum.male.value,
        "height_cm": 160,
        "weight_kg": 50,
        "fitness_level": FitnessLevelEnum.beginner.value,
        "primary_goal": PrimaryGoalEnum.maintain_health.value,
    }
    body = {
        "user": user,
        "profile": profile,
    }

    response = client.post("/v1/users/sign-up", json=body)
    assert response.status_code == 201
    assert response.json()["user"]["email"] == email

    response = client.post("/v1/users/sign-up", json=body)
    assert response.status_code == 409
    assert response.json()["detail"] == "Duplicated email. User was not created."

    # cleaning up
    delete_user_db(db_session, email=email)
