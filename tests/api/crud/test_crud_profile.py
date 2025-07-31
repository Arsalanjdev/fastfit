from datetime import date, datetime, timezone
from decimal import Decimal

import pytest

from src.api.crud.profile import (
    get_profile_by_email,
    get_profile_by_id,
    update_profile_field,
)
from src.api.crud.users import create_user_with_profile
from src.api.models.enums import FitnessLevelEnum, GenderEnum, PrimaryGoalEnum


@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "password": "securepassword",
        "birth_date": date(1970, 1, 1),
        "height_cm": 180.0,
        "weight_kg": 75.0,
        "fitness_level": FitnessLevelEnum.beginner,
        "primary_goal": PrimaryGoalEnum.maintain_health,
        "gender": GenderEnum.male,
        "preferences": {"workout_time": "morning"},
    }


def test_get_profile_by_id(db_session, test_user_data):
    user, profile = create_user_with_profile(db_session, **test_user_data)
    profile_fetched = get_profile_by_id(db_session, id=profile.profile_id)
    assert profile_fetched is not None
    assert profile_fetched.profile_id == profile.profile_id
    db_session.delete(profile)
    db_session.delete(user)
    db_session.commit()


def test_get_profile_by_email(db_session, test_user_data):
    user, profile = create_user_with_profile(db_session, **test_user_data)
    profile_fetched = get_profile_by_email(db_session, email=profile.user.email)
    assert profile_fetched is not None
    assert profile_fetched.profile_id == profile.profile_id
    db_session.delete(profile)
    db_session.delete(user)
    db_session.commit()


def test_update_profile_field_success(db_session, test_user_data):
    user, profile = create_user_with_profile(db_session, **test_user_data)

    old_updated_at = profile.updated_at

    updated_profile = update_profile_field(
        db_session, profile, "height_cm", Decimal("180.5")
    )

    assert updated_profile.height_cm == Decimal("180.5")
    assert updated_profile.updated_at != old_updated_at
    db_session.delete(profile)
    db_session.delete(user)
    db_session.commit()


def test_update_profile_field_invalid_field(db_session, test_user_data):
    user, profile = create_user_with_profile(db_session, **test_user_data)

    with pytest.raises(AttributeError) as excinfo:
        update_profile_field(db_session, profile, "nonexistent_field", "value")
    assert "User Profile doesn't have a nonexistent_field column." in str(excinfo.value)
    db_session.delete(profile)
    db_session.delete(user)
    db_session.commit()


def test_update_profile_field_updated_at_changes(db_session, test_user_data):
    user, profile = create_user_with_profile(db_session, **test_user_data)

    old_updated_at = profile.updated_at
    updated_profile = update_profile_field(db_session, profile, "gender", "male")

    assert updated_profile.gender == "male"
    assert updated_profile.updated_at != old_updated_at
    assert (datetime.now(timezone.utc) - updated_profile.updated_at).total_seconds() < 5
    db_session.delete(profile)
    db_session.delete(user)
    db_session.commit()


#
# def test_delete_profile(db_session, test_user_data):
#     user, profile = create_user_with_profile(db_session, **test_user_data)
#     db_session.commit()
#     db_session.refresh(profile)
#
#     result = delete_profile_from_db(db_session, profile)
#
#     assert result
#     assert (
#         db_session.query(UserProfile)
#         .filter(UserProfile.profile_id == profile.profile_id)
#         .first()
#         is None
#     )
#     db_session.delete(profile)
#     db_session.delete(user)
#     db_session.commit()
