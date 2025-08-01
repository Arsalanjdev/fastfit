from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.api.models.enums import DifficultyEnum


class ExerciseBase(BaseModel):
    name: Annotated[
        str, Field(description="Exercise name", min_length=3, max_length=100)
    ]
    description: Annotated[
        Optional[str], Field(description="Exercise description", default=None)
    ]
    muscle_group: Annotated[
        str,
        Field(
            description="Muscle group",
            min_length=3,
            max_length=50,
        ),
    ]
    equipment_required: Annotated[
        Optional[list[str]],
        Field(
            description="Equipments that are required for the exercise",
            default_factory=list,
        ),
    ]
    difficulty: Annotated[
        DifficultyEnum,
        Field(
            description="Difficulty of the exercise",
            default=DifficultyEnum.BEGINNER,
        ),
    ]


class ExerciseRead(ExerciseBase):
    exercise_id: Annotated[UUID, Field(description="Exercise UUID")]


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(BaseModel):
    name: Annotated[
        Optional[str],
        Field(description="Exercise name", min_length=3, max_length=100, default=None),
    ]
    description: Annotated[
        Optional[str], Field(description="Exercise description", default=None)
    ]
    muscle_group: Annotated[
        Optional[str],
        Field(description="Muscle group", min_length=3, max_length=50, default=None),
    ]
    equipment_required: Annotated[
        Optional[list[str]],
        Field(
            description="Equipments that are required for the exercise",
            default=None,  # None means omitted in partial update
        ),
    ]
    difficulty: Annotated[
        Optional[DifficultyEnum],
        Field(description="Difficulty of the exercise", default=None),
    ]
