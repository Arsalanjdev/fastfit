import uuid
from typing import List, Optional

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.api.models.enums import DifficultyEnum
from src.api.models.exercises import Exercise


def find_duplicated_exercise(
    db: Session,
    *,
    name: str,
    muscle_group: str,
    difficulty: DifficultyEnum,
    equipment_required: Optional[list[str]] | None = None,
    description: Optional[str] | None = None,
) -> Exercise | None:
    """
    Check if exercise with all the specifications already exists.
    :param db:
    :param name:
    :param muscle_group:
    :param difficulty:
    :param equipment_required:
    :param description:
    :return:
    """
    existing = (
        db.query(Exercise)
        .filter(
            Exercise.name == name,
            Exercise.muscle_group == muscle_group,
            Exercise.difficulty == difficulty,
            Exercise.equipment_required == equipment_required,
            Exercise.description == description,
        )
        .first()
    )
    return existing


def create_exercise_db(
    db: Session,
    *,
    name: str,
    muscle_group: str,
    difficulty: DifficultyEnum,
    equipment_required: Optional[list[str]] | None = None,
    description: Optional[str] | None = None,
) -> Exercise:
    existing = find_duplicated_exercise(
        db,
        name=name,
        muscle_group=muscle_group,
        difficulty=difficulty,
        equipment_required=equipment_required,
        description=description,
    )
    if existing:
        raise ValueError("An identical exercise already exists.")
    exercise = Exercise(
        name=name,
        muscle_group=muscle_group,
        difficulty=difficulty,
        equipment_required=equipment_required,
        description=description,
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def get_exercise_by_id(db: Session, exercise_id: uuid.UUID) -> Exercise | None:
    return db.get(Exercise, exercise_id)


def get_exercises_by_name(db: Session, name: str) -> List[Exercise] | None:
    """
    Returns a list of exercises that shares the same name.
    :param db:
    :param name:
    :return: List of exercises
    """
    return db.query(Exercise).filter(Exercise.name == name).all()


def get_exercises_by_difficulty(db: Session, difficulty: str) -> List[Exercise] | None:
    """
    Returns a list of exercises that share the same difficulty.
    :param db:
    :param difficulty:
    :return:
    """
    return db.query(Exercise).filter(Exercise.difficulty == difficulty).all()


def get_exercises_by_muscle_group(
    db: Session, muscle_group: str
) -> List[Exercise] | None:
    """
    Returns a list of exercises that share the same muscle group focus.
    :return:
    """
    return db.query(Exercise).filter(Exercise.muscle_group == muscle_group).all()


def update_exercise_db(
    db: Session,
    exercise: Exercise,
    field_name: str,
    value,
) -> Exercise:
    """
    updates an exercise field.
    :param db:
    :param exercise:
    :param field_name:
    :param value:
    :return:
    """
    if not hasattr(exercise, field_name):
        raise AttributeError(f"Exercise doesn't have a {field_name} column.")

    setattr(exercise, field_name, value)
    db.commit()
    db.refresh(exercise)
    return exercise


def delete_exercise_db(db: Session, exercise_id: uuid.UUID) -> bool:
    """
    Deletes an exercise.
    :param db:
    :param exercise_id:
    :return: True if exercise was deleted. False otherwise.
    """
    to_delete = get_exercise_by_id(db, exercise_id)
    if to_delete is None:
        return False
    db.delete(to_delete)
    db.commit()
    return True


def get_all_exercises_db(db: Session, limit: int, offset: int) -> List[Exercise]:
    """
    Returns a list of exercises limited by limit and offseted.
    :param db:
    :param limit:
    :param offset:
    :return:
    """
    query = select(Exercise).offset(offset).limit(limit)
    return db.execute(query).scalars().all()
