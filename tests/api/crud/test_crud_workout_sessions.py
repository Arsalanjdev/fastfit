from datetime import date, datetime
from typing import Any

import pytest

from src.api.crud.users import create_user_with_profile
from src.api.crud.workout_sessions import (
    create_workout_session,
    delete_workout_session,
    get_all_workout_sessions_by_user,
    update_workout_session_field,
)
from src.api.models.enums import FitnessLevelEnum, GenderEnum, PrimaryGoalEnum
from tests.utils import is_iso_datetime


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


def dummy_session() -> dict[str, Any]:
    return {
        "start_time": datetime.now(),
        "perceived_intensity": 5,
        "duration_minutes": 5,
        "notes": "",
        "session_type": "general",
    }


# start_time = Column(DateTime(timezone=True), nullable=True)
#     perceived_intensity = Column(Integer, nullable=True)
#     duration_minutes = Column(Integer, nullable=True)
#     notes = Column(Text, nullable=True)
#     session_type = Column(Text, nullable=True, server_default="general")
#


def test_crud_workout_sessions_create(db_session, test_user_data):
    """
    Tests creating a workout session.
    :param db_session:
    :return:
    """
    dummy_user = test_user_data.copy()
    session = dummy_session()
    user, _ = create_user_with_profile(db_session, **dummy_user)
    workout_session = create_workout_session(
        db_session, user_id=user.user_id, **session
    )
    assert workout_session.user_id == user.user_id
    assert workout_session.perceived_intensity == session["perceived_intensity"]
    assert workout_session.duration_minutes == session["duration_minutes"]
    assert workout_session.notes == session["notes"]
    assert workout_session.session_type == session["session_type"]
    db_session.delete(user)
    db_session.commit()


def test_crud_get_all_workout_sessions_by_user(db_session, test_user_data):
    user, _ = create_user_with_profile(db_session, **test_user_data)
    dummy_session_data = dummy_session()
    create_workout_session(db_session, user_id=user.user_id, **dummy_session_data())
    create_workout_session(db_session, user_id=user.user_id, **dummy_session_data())

    other_user, _ = create_user_with_profile(db_session, **test_user_data)
    create_workout_session(
        db_session, user_id=other_user.user_id, **dummy_session_data()
    )

    sessions = get_all_workout_sessions_by_user(db_session, user.user_id)

    assert len(sessions) >= 2
    for s in sessions:
        assert s.user_id == user.user_id
    db_session.delete(user)
    db_session.commit()


def test_crud_update_workout_session_field(db_session, test_user_data):
    user, _ = create_user_with_profile(db_session, **test_user_data)
    dummy_session_data = dummy_session()
    workout_session = create_workout_session(
        db_session, user_id=user.user_id, **dummy_session_data
    )

    new_notes = "Updated notes"
    updated_session = update_workout_session_field(
        db_session, workout_session, "notes", new_notes
    )

    assert updated_session.notes == new_notes

    # Also test invalid field update raises AttributeError
    with pytest.raises(AttributeError):
        update_workout_session_field(
            db_session, workout_session, "invalid_field", "value"
        )
    db_session.delete(user)
    db_session.commit()


def test_crud_delete_workout_session(db_session, test_user_data):
    user, _ = create_user_with_profile(db_session, **test_user_data)
    dummy_session_data = dummy_session()
    session_data = dummy_session_data()
    workout_session = create_workout_session(
        db_session, user_id=user.user_id, **session_data
    )

    result = delete_workout_session(db_session, workout_session.session_id)
    assert result is True

    result = delete_workout_session(db_session, workout_session.session_id)
    assert result is False

    db_session.delete(user)
    db_session.commit()
