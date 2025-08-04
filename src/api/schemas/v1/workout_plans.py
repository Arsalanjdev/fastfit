from datetime import date
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WorkoutPlansBase(BaseModel):
    valid_from: Annotated[date, Field(description="Valid from")]
    valid_to: Annotated[date, Field(description="Valid to")]
    focus_area: Annotated[str, Field(description="Focus area")]
    ai_model_version: Annotated[str, Field(description="AI model version")]
    plan_data: Annotated[
        dict[str, str], Field(description="Plan data generated and sent by the ai")
    ]


class WorkoutPlansCreate(WorkoutPlansBase):
    pass


class WorkoutPlansRead(WorkoutPlansBase):
    plan_id: Annotated[UUID, Field(description="Plans UUID")]
    user_id: Annotated[
        UUID, Field(description="User ID")
    ]  # replace with user itself #TODO
    generated_at: Annotated[date, Field(description="Generated at")]
    model_config = ConfigDict(from_attributes=True)
