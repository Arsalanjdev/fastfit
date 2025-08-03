import hypothesis.strategies as st
import pytest
from hypothesis import given
from pydantic import ValidationError

from src.api.models.enums import DifficultyEnum
from src.api.schemas.v1.exercises import ExerciseCreate, ExerciseRead, ExerciseUpdate
from tests.utils import is_valid_uuid


@given(
    exercise_id=st.uuids(),
    name=st.text(min_size=3, max_size=100),
    description=st.one_of(st.none(), st.text()),
    muscle_group=st.text(min_size=3, max_size=50),
    equipment_required=st.lists(
        st.text(min_size=3, max_size=100),
        min_size=0,
        max_size=50,
    ),
    difficulty=st.sampled_from(list(DifficultyEnum)),
)
def test_schema_exercise_read(
    exercise_id, name, description, muscle_group, equipment_required, difficulty
):
    exercise = {
        "exercise_id": exercise_id,
        "name": name,
        "description": description,
        "muscle_group": muscle_group,
        "equipment_required": equipment_required,
        "difficulty": difficulty,
    }
    validated_exercise = ExerciseRead(**exercise)
    assert is_valid_uuid(validated_exercise.exercise_id)
    assert validated_exercise.exercise_id == exercise_id
    assert validated_exercise.name == name
    assert validated_exercise.description == description
    assert validated_exercise.muscle_group == muscle_group
    assert isinstance(validated_exercise.difficulty, DifficultyEnum)
    assert validated_exercise.difficulty == difficulty
    assert validated_exercise.equipment_required == equipment_required


@given(
    name=st.text(min_size=3, max_size=100),
    description=st.one_of(st.none(), st.text()),
    muscle_group=st.text(min_size=3, max_size=50),
    equipment_required=st.lists(
        st.text(min_size=3, max_size=100),
        min_size=0,
        max_size=50,
    ),
    difficulty=st.sampled_from(list(DifficultyEnum)),
)
def test_schema_exercise_create(
    name, description, muscle_group, equipment_required, difficulty
):
    exercise = {
        "name": name,
        "description": description,
        "muscle_group": muscle_group,
        "equipment_required": equipment_required,
        "difficulty": difficulty,
    }
    validated_exercise = ExerciseCreate(**exercise)
    assert not hasattr(validated_exercise, "user_id")
    assert validated_exercise.name == name
    assert validated_exercise.description == description
    assert validated_exercise.muscle_group == muscle_group
    assert isinstance(validated_exercise.difficulty, DifficultyEnum)
    assert validated_exercise.difficulty == difficulty
    assert validated_exercise.equipment_required == equipment_required


@given(name=st.text(min_size=0, max_size=2))
def test_schema_create_invalid_name_too_short(name):
    with pytest.raises(ValidationError):
        ExerciseCreate(
            name=name,
            muscle_group="Chest",
            equipment_required=[],
            difficulty=DifficultyEnum.BEGINNER,
        )


def test_schema_exercise_create_invalid_difficulty():
    with pytest.raises(ValidationError):
        ExerciseCreate(
            name="Push Up",
            muscle_group="Chest",
            equipment_required=[],
            difficulty="expert",  # invalid enum value
        )


def test_schema_exercise_create_equipment_wrong_type():
    with pytest.raises(ValidationError):
        ExerciseCreate(
            name="Push Up",
            muscle_group="Chest",
            equipment_required=[123, "dumbbell"],
            difficulty=DifficultyEnum.BEGINNER,
        )


def test_schema_exercise_create_missing_required_field():
    with pytest.raises(ValidationError):
        ExerciseCreate(
            name="Push Up",
            equipment_required=[],
            difficulty=DifficultyEnum.BEGINNER,
        )


@given(
    name=st.one_of(st.none(), st.text(min_size=3, max_size=100)),
    description=st.one_of(st.none(), st.text()),
    muscle_group=st.one_of(st.none(), st.text(min_size=3, max_size=50)),
    equipment_required=st.one_of(
        st.none(), st.lists(st.text(min_size=3, max_size=100), max_size=50)
    ),
    difficulty=st.one_of(st.none(), st.sampled_from(list(DifficultyEnum))),
)
def test_schema_valid_exercise_update(
    name, description, muscle_group, equipment_required, difficulty
):
    data = {}
    if name is not None:
        data["name"] = name
    if description is not None:
        data["description"] = description
    if muscle_group is not None:
        data["muscle_group"] = muscle_group
    if equipment_required is not None:
        data["equipment_required"] = equipment_required
    if difficulty is not None:
        data["difficulty"] = difficulty

    update_obj = ExerciseUpdate(**data)
    # If provided, field values should match
    if "name" in data:
        assert update_obj.name == data["name"]
    if "description" in data:
        assert update_obj.description == data["description"]
    if "muscle_group" in data:
        assert update_obj.muscle_group == data["muscle_group"]
    if "equipment_required" in data:
        assert update_obj.equipment_required == data["equipment_required"]
    if "difficulty" in data:
        assert update_obj.difficulty == data["difficulty"]


@pytest.mark.parametrize(
    "field, value",
    [
        ("name", "ab"),  # too short (min_length=3)
        ("muscle_group", ""),  # too short (min_length=3)
        ("equipment_required", [123, "dumbbell"]),  # wrong type in list
        ("difficulty", "expert"),  # invalid enum value
    ],
)
def test_schema_invalid_exercise_update(field, value):
    data = {field: value}
    with pytest.raises(ValidationError):
        ExerciseUpdate(**data)
