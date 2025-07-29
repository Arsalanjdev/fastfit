import uuid
from datetime import datetime

import httpx
from fastapi.encoders import jsonable_encoder

from tests.factories.models import get_random_user_dict


def mock_output(return_value=None):
    return lambda *args, **kwargs: return_value


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

    def get_user_by_email(*args, **kwargs):
        return None

    def create_user(*args, **kwargs):
        return {
            "uuid": uuid.uuid4(),
            "email": random_user.get("email"),
            "created_at": random_user.get("created_at"),
            "is_active": True,
            "role": "user",
        }

    monkeypatch.setattr("src.api.crud.users.get_user_by_email", get_user_by_email)
    monkeypatch.setattr("src.api.crud.users.create_user_db", create_user)

    subset_keys = {"email", "password"}
    body_create = {k: random_user[k] for k in subset_keys if k in random_user}
    json_data = jsonable_encoder(body_create)

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
