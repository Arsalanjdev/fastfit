import uuid
from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

# start_time = Column(DateTime(timezone=True), nullable=True)
# perceived_intensity = Column(Integer, nullable=True)
# duration_minutes = Column(Integer, nullable=True)
# notes = Column(Text, nullable=True)
# session_type = Column(Text, nullable=True, server_default="general")


class WorkoutSession(BaseModel):
    start_time: Annotated[
        Optional[datetime],
        Field(
            default_factory=datetime.now,
            description="Start time of the workout session",
        ),
    ]
    perceived_intensity: Annotated[
        Optional[int],
        Field(
            default=1,
            description="Perceived intensity of the workout session",
            ge=1,
            le=10,
        ),
    ]
    duration_minutes: Annotated[
        Optional[int],
        Field(
            default=1,
            description="Duration of the workout session",
            ge=1,
            le=1000,
        ),
    ]
    notes: Annotated[
        Optional[str],
        Field(
            default=None,
            description="Note about the workout session",
            min_length=3,
            max_length=1000,
        ),
    ]
    session_type: Annotated[
        Optional[str],
        Field(
            default=None,
            description="Session type of the workout session",
            min_length=3,
            max_length=100,
        ),
    ]

    @field_validator("start_time", mode="before")
    @classmethod
    def validate_strict_datetime(cls, v):
        if v is not None and not isinstance(v, datetime):
            raise TypeError("start_time must be a datetime object")
        return v


class WorkoutSessionCreate(WorkoutSession):
    pass


class WorkoutSessionRead(WorkoutSession):
    session_id: Annotated[uuid.UUID, Field(description="The Session Id")]
    user_id: Annotated[uuid.UUID, Field(description="The User Id")]
    # exercises: Annotated[WorkoutSession] #TODO
    model_config = ConfigDict(from_attributes=True)


class WorkoutSessionUpdate(WorkoutSession):
    pass


class WorkoutSessionDelete(WorkoutSession):
    session_id: Annotated[uuid.UUID, Field(description="The Session Id")]
