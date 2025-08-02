import uuid
from typing import Any

import pytest

from src.api.crud.exercises import (
    create_exercise_db,
    delete_exercise,
    get_exercise_by_id,
    get_exercises_by_difficulty,
    get_exercises_by_muscle_group,
    get_exercises_by_name,
    update_exercise_field,
)
from src.api.models.enums import DifficultyEnum
from tests.utils import is_valid_uuid


def dummy_exercise() -> dict[str, Any]:
    """
    :return: returns a dummy exercise dictionary.
    """
    return {
        "name": "bench press",
        "description": "A classic chest exercise using a barbell.",
        "muscle_group": "Chest",
        "equipment_required": ["barbell", "bench"],
        "difficulty": DifficultyEnum.BEGINNER.value,
    }


def test_crud_create_exercise(db_session) -> None:
    """
    Tests creating an exercise and commiting it to the database.
    :param db:
    :return:
    """
    exercise = dummy_exercise()
    exercise_db = create_exercise_db(db_session, **exercise)
    assert hasattr(exercise_db, "exercise_id")
    assert exercise_db.exercise_id is not None
    assert is_valid_uuid(exercise_db.exercise_id)
    assert isinstance(exercise_db.difficulty, DifficultyEnum)
    assert exercise_db.difficulty == exercise.get("difficulty")
    assert exercise_db.description == exercise.get("description")
    assert exercise_db.muscle_group == exercise.get("muscle_group")
    assert exercise_db.equipment_required == exercise.get("equipment_required")
    db_session.delete(exercise_db)
    db_session.commit()


def test_crud_get_exercise_by_id(db_session) -> None:
    """
    Tests getting an exercise from the database by its name.
    :param db_session:
    :return:
    """
    exercise = dummy_exercise()
    exercise_db = create_exercise_db(db_session, **exercise)
    exercise_fetched = get_exercise_by_id(db_session, exercise_db.exercise_id)
    assert exercise_fetched is not None
    assert exercise_fetched.description == exercise.get("description")
    assert exercise_db.muscle_group == exercise.get("muscle_group")
    assert exercise_db.equipment_required == exercise.get("equipment_required")
    assert is_valid_uuid(exercise_fetched.exercise_id)
    assert isinstance(exercise_fetched.difficulty, DifficultyEnum)
    db_session.delete(exercise_db)
    db_session.commit()


def test_crud_get_exercises_by_name(db_session) -> None:
    """
    Tests getting exercises sharing the same name from the database by their name.
    :param db_session:
    :return:
    """

    exercise_data = dummy_exercise()
    exercise_data_2 = exercise_data.copy()
    exercise_data_2["description"] = (
        "test"  # it should not be completely identical to exercise_data
    )

    exercise1 = create_exercise_db(db_session, **exercise_data)
    exercise2 = create_exercise_db(db_session, **exercise_data_2)

    exercises = get_exercises_by_name(db_session, exercise_data["name"])

    # Type narrowing: ensure exercises is not None (should never be None here)
    assert exercises is not None, "Expected exercises to be a list, but got None"

    assert len(exercises) >= 2
    assert all(ex.name == exercise_data["name"] for ex in exercises)
    assert any(ex.exercise_id == exercise1.exercise_id for ex in exercises)
    assert any(ex.exercise_id == exercise2.exercise_id for ex in exercises)

    db_session.delete(exercise1)
    db_session.delete(exercise2)
    db_session.commit()


def test_crud_get_exercises_by_difficulty(db_session) -> None:
    """
    Tests getting exercises by difficulty from the database.
    """
    exercise_data = dummy_exercise()
    exercise_data_2 = exercise_data.copy()
    exercise_data_2["description"] = "test"  # slightly different description

    exercise1 = create_exercise_db(db_session, **exercise_data)
    exercise2 = create_exercise_db(db_session, **exercise_data_2)

    exercises = get_exercises_by_difficulty(db_session, exercise_data["difficulty"])

    # Type narrowing: ensure exercises is not None (should never be None here)
    assert exercises is not None, "Expected exercises to be a list, but got None"

    assert len(exercises) >= 2
    assert all(ex.difficulty == exercise_data["difficulty"] for ex in exercises)
    assert any(ex.exercise_id == exercise1.exercise_id for ex in exercises)
    assert any(ex.exercise_id == exercise2.exercise_id for ex in exercises)

    db_session.delete(exercise1)
    db_session.delete(exercise2)
    db_session.commit()


def test_crud_get_exercises_by_muscle_group(db_session) -> None:
    """
    Tests getting exercises by muscle group from the database.
    """
    exercise_data = dummy_exercise()
    exercise1 = create_exercise_db(db_session, **exercise_data)

    exercise_data_2 = exercise_data.copy()
    exercise_data_2["name"] = "push up"
    exercise2 = create_exercise_db(db_session, **exercise_data_2)

    exercises = get_exercises_by_muscle_group(db_session, exercise_data["muscle_group"])

    # Type narrowing: ensure exercises is not None (should never be None here)
    assert exercises is not None, "Expected exercises to be a list, but got None"

    assert len(exercises) >= 2
    assert all(ex.muscle_group == exercise_data["muscle_group"] for ex in exercises)
    assert any(ex.exercise_id == exercise1.exercise_id for ex in exercises)
    assert any(ex.exercise_id == exercise2.exercise_id for ex in exercises)

    db_session.delete(exercise1)
    db_session.delete(exercise2)
    db_session.commit()


def test_update_exercise_field_success(db_session) -> None:
    exercise = dummy_exercise()
    exercise["difficulty"] = DifficultyEnum.BEGINNER.value
    exercise_db = create_exercise_db(db_session, **exercise)

    original_difficulty = exercise_db.difficulty

    exercise_updated = update_exercise_field(
        db_session, exercise_db, "difficulty", DifficultyEnum.INTERMEDIATE.value
    )

    assert exercise_updated.exercise_id == exercise_db.exercise_id
    assert exercise_updated.difficulty != original_difficulty
    assert exercise_updated.difficulty == DifficultyEnum.INTERMEDIATE

    db_session.delete(exercise_updated)
    db_session.commit()


def test_update_exercise_field_failure(db_session) -> None:
    """
    Tests that updating a non-existent field on an exercise raises an AttributeError.
    """
    exercise_data = dummy_exercise()
    exercise_db = create_exercise_db(db_session, **exercise_data)

    with pytest.raises(AttributeError) as exc_info:
        update_exercise_field(db_session, exercise_db, "non_existent_field", "value")

    assert "doesn't have a non_existent_field column" in str(exc_info.value)

    db_session.delete(exercise_db)
    db_session.commit()


def test_delete_exercise(db_session) -> None:
    """
    Tests deleting an exercise.
    :param db_session:
    :return:
    """
    exercise = dummy_exercise()
    exercise_db = create_exercise_db(db_session, **exercise)
    id = exercise_db.exercise_id
    is_deleted = delete_exercise(db_session, exercise_db.exercise_id)
    assert is_deleted
    assert get_exercise_by_id(db_session, id) is None


def test_delete_exercise_non_existent(db_session) -> None:
    """
    Tests deleting an exercise that does not exist.
    :param db_session:
    :return:
    """
    id = uuid.uuid4()
    to_delete = delete_exercise(db_session, id)
    assert to_delete is False
