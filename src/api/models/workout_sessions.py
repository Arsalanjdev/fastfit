from uuid import uuid4

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    session_id = Column(
        UUID(as_uuid=True), nullable=False, default=uuid4, primary_key=True
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=True)
    perceived_intensity = Column(Integer, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    session_type = Column(Text, nullable=True, default="general")

    __table_args__ = (
        CheckConstraint(
            "perceived_intensity BETWEEN 1 AND 10",
            name="check_perceived_intensity_range",
        ),
        Index("idx_user_sessions", "user_id"),
    )


1
