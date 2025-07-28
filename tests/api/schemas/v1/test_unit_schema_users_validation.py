from datetime import datetime

from src.api.schemas.v1.users import UserRead


def test_schema_users_read():
    time = datetime.now()
    valid_data = {
        "email": "example@example.com",
        "is_active": True,
        "created_at": time,
    }
    read_user = UserRead(**valid_data)
    assert read_user.email == "example@example.com"
    assert read_user.is_active
    assert read_user.created_at == time
