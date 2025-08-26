import json
from datetime import date

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from src.api.crud.users import delete_user_db
from src.api.models.enums import FitnessLevelEnum, GenderEnum, PrimaryGoalEnum


def test_integration_authentication_success(
    db_session: Session, client: TestClient, user_factory
):
    # create user
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

    response = client.post(
        "/v1/users/sign-up",
        json=body,
    )
    assert response.status_code == 201
    assert response.json()["user"]["email"] == email

    # authenticating the user
    response = client.post("/token", data={"username": email, "password": password})
    data = response.json()
    assert response.status_code == 200
    assert "token_type" in data
    assert "user_id" in data
    assert delete_user_db(db_session, email=email)
