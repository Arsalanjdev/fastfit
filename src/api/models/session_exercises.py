from uuid import uuid4

from sqlalchemy import (
    Column,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class SessionExercises(Base):
    __tablename__ = "session_exercises"

    session_exercise_id = Column(
        UUID(as_uuid=True), nullable=False, default=uuid4, primary_key=True
    )
    session_id = Column(
        UUID(as_uuid=True), ForeignKey("workout_sessions.session_id"), nullable=False
    )
    exercise_id = Column(
        UUID(as_uuid=True), ForeignKey("exercises.exercise_id"), nullable=False
    )
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    weight_kg = Column(Numeric(5, 2), nullable=True)
    distance_km = Column(Numeric(4, 2), nullable=True)
    notes = Column(Text, nullable=True)

    session = relationship("WorkoutSession", back_populates="exercise")
    exercise = relationship("Exercise", back_populates="session_exercises")

    __table_args__ = (
        UniqueConstraint("session_id", "exercise_id", name="uq_session_exercise"),
        Index("idx_session_exercises", "session_id"),
    )
