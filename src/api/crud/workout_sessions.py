import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from src.api.models.workout_sessions import WorkoutSession

# user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
#     start_time = Column(DateTime(timezone=True), nullable=True)
#     perceived_intensity = Column(Integer, nullable=True)
#     duration_minutes = Column(Integer, nullable=True)
#     notes = Column(Text, nullable=True)
#     session_type = Column(Text, nullable=True, server_default="


def create_workout_session(
    db: Session,
    *,
    user_id: UUID,
    start_time: datetime | None = None,
    perceived_intensity: int | None = 1,
    duration_minutes: int | None = 1,
    notes: str | None = None,
    session_type: str | None = None,
) -> WorkoutSession:
    if not start_time:
        start_time = datetime.now()
    session_id = uuid.uuid4()
    session = WorkoutSession(
        session_id=session_id,
        user_id=user_id,
        start_time=start_time,
        perceived_intensity=perceived_intensity,
        duration_minutes=duration_minutes,
        notes=notes,
        session_type=session_type,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_workout_session(db: Session, session_id: UUID) -> WorkoutSession:
    return db.query(WorkoutSession).get(session_id)


def get_all_workout_sessions_by_user(
    db: Session, user_id: UUID
) -> list[WorkoutSession]:
    return db.query(WorkoutSession).filter(WorkoutSession.user_id == user_id).all()


def update_workout_session_field(
    db: Session,
    workout_session: WorkoutSession,
    field_name: str,
    value: str,
):
    if not hasattr(workout_session, field_name):
        raise AttributeError(f"No {field_name} in {workout_session} found.")

    setattr(workout_session, field_name, value)
    db.commit()
    db.refresh(workout_session)
    return workout_session


def delete_workout_session(db: Session, session_id: UUID) -> bool:
    workout_session = get_workout_session(db, session_id)
    if not workout_session:
        return False
    db.delete(workout_session)
    db.commit()
    return True
