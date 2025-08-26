from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from src import WorkoutPlans


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
    uuid = uuid4()
    generated_at = datetime.now().isoformat()
    workout_plan = WorkoutPlans(
        user_id=user_id,
        valid_from=valid_from,
        valid_to=valid_to,
        focus_area=focus_area,
        ai_model_version=ai_model_version,
        plan_data=plan_data,
        plan_id=uuid,
        generated_at=generated_at,
    )
    db.add(workout_plan)
    db.commit()
    db.refresh(workout_plan)
    return workout_plan


def get_workout_plans_by_user_id(
    db_session: Session, user_id: UUID | None = None
) -> list[WorkoutPlans]:
    if not user_id:
        raise ValueError("user_id is required.")

    plans = db_session.query(WorkoutPlans).filter_by(user_id=user_id).all()
    return plans
