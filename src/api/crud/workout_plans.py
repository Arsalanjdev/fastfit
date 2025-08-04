from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session


def get_workout_plan_by_id(db: Session, workout_plan_id: UUID):
    pass


def create_workout_plan_db(
    db: Session,
    *,
    user_id=UUID,
    valid_from: date,
    valid_to: date,
    focus_area: str,
    ai_model_version: str,
    plan_data: dict,
):
    pass
