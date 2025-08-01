from typing import Optional

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
            name == name,
            muscle_group == muscle_group,
            difficulty == difficulty,
            equipment_required == equipment_required,
            description == description,
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
