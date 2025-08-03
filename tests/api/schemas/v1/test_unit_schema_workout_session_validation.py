from datetime import datetime
from uuid import UUID

import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.strategies import none, one_of
from pydantic import ValidationError

from src.api.schemas.v1.workout_sessions import (
    WorkoutSessionCreate,
    WorkoutSessionDelete,
    WorkoutSessionRead,
    WorkoutSessionUpdate,
)

# start_time = Column(DateTime(timezone=True), nullable=True)
# perceived_intensity = Column(Integer, nullable=True)
# duration_minutes = Column(Integer, nullable=True)
# notes = Column(Text, nullable=True)
# session_type = Column(Text, nullable=True, server_default="general")


@given(
    start_time=one_of(none(), st.datetimes()),
    perceived_intensity=one_of(none(), st.integers(min_value=1, max_value=10)),
    duration_minutes=one_of(none(), st.integers(min_value=1, max_value=1000)),
    notes=one_of(none(), st.text(min_size=3, max_size=1000)),
    session_type=one_of(none(), st.text(min_size=3, max_size=100)),
)
def test_schema_create_workout_session(
    start_time, perceived_intensity, duration_minutes, notes, session_type
):
    dummy_session = {
        "start_time": start_time,
        "perceived_intensity": perceived_intensity,
        "duration_minutes": duration_minutes,
        "notes": notes,
        "session_type": session_type,
    }
    validated_session = WorkoutSessionCreate(**dummy_session)
    assert validated_session.start_time == start_time
    assert validated_session.perceived_intensity == perceived_intensity
    assert validated_session.duration_minutes == duration_minutes
    assert validated_session.notes == notes
    assert validated_session.session_type == session_type


@given(perceived_intensity=one_of(st.integers(max_value=0), st.integers(min_value=11)))
def test_schema_create_workout_session_invalid_perceived_intensity(perceived_intensity):
    data = {"perceived_intensity": perceived_intensity}
    with pytest.raises(ValidationError):
        WorkoutSessionCreate(**data)


@given(duration_minutes=one_of(st.integers(max_value=0), st.floats()))
def test_schema_create_workout_session_invalid_duration_minutes(duration_minutes):
    data = {"duration_minutes": duration_minutes}
    with pytest.raises(ValidationError):
        WorkoutSessionCreate(**data)


@given(start_time=one_of(st.integers(), st.floats()))
def test_schema_create_workout_session_invalid_start_time(start_time):
    with pytest.raises((ValidationError, TypeError)):
        WorkoutSessionCreate(start_time=start_time)


@given(notes=one_of(st.text(min_size=0, max_size=2), st.integers(), st.floats()))
def test_schema_create_workout_session_invalid_notes(notes):
    data = {"notes": notes}
    with pytest.raises(ValidationError):
        WorkoutSessionCreate(**data)


@given(
    session_type=one_of(
        st.text(min_size=0, max_size=2), st.text(min_size=101), st.integers()
    )
)
def test_schema_create_workout_session_invalid_session_type(session_type):
    data = {"session_type": session_type}
    with pytest.raises(ValidationError):
        WorkoutSessionCreate(**data)


@given(
    session_id=st.uuids(),
    start_time=st.datetimes(),
)
def test_schema_workout_session_read_valid(session_id, start_time):
    data = {
        "session_id": session_id,
        "start_time": start_time,
    }
    # Add minimal required fields with defaults or valid dummy values
    data.update(
        {
            "perceived_intensity": 5,
            "duration_minutes": 30,
            "notes": "Some notes",
            "session_type": "general",
        }
    )
    session = WorkoutSessionRead(**data)
    assert isinstance(session.session_id, UUID)
    assert session.start_time == start_time


@pytest.mark.parametrize("invalid_session_id", ["not-a-uuid", 123, None, ""])
def test_schema_workout_session_read_invalid_session_id(invalid_session_id):
    data = {
        "session_id": invalid_session_id,
        "start_time": datetime.now(),
        "perceived_intensity": 5,
        "duration_minutes": 30,
        "notes": "Some notes",
        "session_type": "general",
    }
    with pytest.raises(ValidationError):
        WorkoutSessionRead(**data)


@given(
    start_time=st.one_of(st.none(), st.datetimes()),
    perceived_intensity=st.one_of(st.none(), st.integers(min_value=1, max_value=10)),
    duration_minutes=st.one_of(st.none(), st.integers(min_value=1, max_value=1000)),
    notes=st.one_of(st.none(), st.text(min_size=3, max_size=1000)),
    session_type=st.one_of(st.none(), st.text(min_size=3, max_size=100)),
)
def test_schema_workout_session_update_valid(
    start_time, perceived_intensity, duration_minutes, notes, session_type
):
    data = {
        k: v
        for k, v in {
            "start_time": start_time,
            "perceived_intensity": perceived_intensity,
            "duration_minutes": duration_minutes,
            "notes": notes,
            "session_type": session_type,
        }.items()
        if v is not None
    }
    update = WorkoutSessionUpdate(**data)
    for key, val in data.items():
        assert getattr(update, key) == val


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("perceived_intensity", 0),
        ("perceived_intensity", 11),
        ("duration_minutes", 0),
        ("notes", "ab"),  # less than min length 3
        ("session_type", "ab"),
    ],
)
def test_schema_workout_session_update_invalid_fields(field, invalid_value):
    data = {field: invalid_value}
    with pytest.raises(ValidationError):
        WorkoutSessionUpdate(**data)


@given(session_id=st.uuids())
def test_schema_workout_session_delete_valid(session_id):
    data = {"session_id": session_id}
    delete = WorkoutSessionDelete(**data)
    assert delete.session_id == session_id


@pytest.mark.parametrize("invalid_session_id", ["not-a-uuid", 123, None, ""])
def test_schema_workout_session_delete_invalid_session_id(invalid_session_id):
    data = {"session_id": invalid_session_id}
    with pytest.raises(ValidationError):
        WorkoutSessionDelete(**data)
