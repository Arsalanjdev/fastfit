from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.api.models.enums import FitnessLevelEnum, GenderEnum, PrimaryGoalEnum


class UserProfileBase(BaseModel):
    birth_date: Annotated[date, Field(description="Date of birth")] = date(1970, 1, 1)
    gender: Annotated[GenderEnum, Field(description="Gender of the user")] = (
        GenderEnum.unspecified
    )
    height_cm: Annotated[
        Decimal,
        Field(
            description="Height of the user in centimeters",
            max_digits=5,
            decimal_places=2,
            ge=40,
            le=230,
        ),
    ]
    weight_kg: Annotated[
        Decimal,
        Field(
            description="Weight of the user in centimeters",
            max_digits=5,
            decimal_places=2,
            ge=10,
            le=650,
        ),
    ]
    fitness_level: Annotated[
        FitnessLevelEnum, Field(description="Fitness level of the user")
    ]
    primary_goal: Annotated[
        PrimaryGoalEnum, Field(description="Primary goal of the user")
    ]
    medical_conditions: Annotated[
        Optional[str], Field(description="Medical conditions of the user")
    ] = ""
    preferences: Annotated[
        Optional[dict], Field(description="Preferences of the user")
    ] = dict()


class UserProfileRead(UserProfileBase):
    profile_id: Annotated[UUID, Field(description="UUID of the user's profile")]
    user_id: Annotated[UUID, Field(description="UUID of the user")]
    updated_at: Annotated[
        datetime, Field(description="Updated at of the user's profile")
    ]
    model_config = ConfigDict(from_attributes=True)


class UserProfileCreate(UserProfileBase):
    pass
