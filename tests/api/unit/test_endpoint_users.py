import uuid
from datetime import datetime

import httpx
from fastapi.encoders import jsonable_encoder

from tests.factories.models import get_random_user_dict


def is_valid_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except (ValueError, TypeError):
        return False


def is_iso_datetime(s: str) -> bool:
    try:
        datetime.fromisoformat(s.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def test_endpoint_users_create(client: httpx.Client, monkeypatch):
    random_user = get_random_user_dict()

    def create_user(*args, **kwargs):
        return {
            "user_id": uuid.uuid4(),
            "email": random_user.get("email"),
            "created_at": datetime.now().isoformat(),
            "is_active": True,
            "role": "user",
        }

    monkeypatch.setattr("src.api.routers.users.create_user_db", create_user)

    keys = {"email", "password"}
    random_user = {key: random_user[key] for key in keys}
    json_data = jsonable_encoder(random_user)

    response = client.post("/v1/users/sign-up", json=json_data)
    response_dict: dict[str, str] = response.json()

    user_id = response_dict.get("user_id")
    created_at = response_dict.get("created_at")

    assert response.status_code == 201
    assert user_id is not None and is_valid_uuid(user_id)
    assert response_dict.get("email") == json_data.get("email")
    assert "password" not in response_dict
    assert created_at is not None and is_iso_datetime(created_at)
    assert response_dict.get("role") in ["user", "coach", "admin"]
    assert response_dict.get("is_active")


def test_endpoint_users_signup_missing_email(client):
    response = client.post("/v1/users/sign-up", json={"password": "dawiooYAR(W*Y%124"})
    assert response.status_code == 422
