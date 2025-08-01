from typing import Any

from src.api.crud.exercises import create_exercise_db
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
