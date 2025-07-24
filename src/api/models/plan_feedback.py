from uuid import uuid4

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class PlanFeedback(Base):
    __tablename__ = "plan_feedback"

    feedback_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    plan_id = Column(
        UUID(as_uuid=True), ForeignKey("workout_plans.plan_id"), nullable=False
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    completion_percentage = Column(Integer, server_default=text("0"), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    effectiveness_rating = Column(Integer, nullable=True)

    plan = relationship("WorkoutPlans", back_populates="feedback")
    user = relationship("User", back_populates="feedback")

    __table_args__ = (
        CheckConstraint(
            "completion_percentage BETWEEN 0 AND 100",
            name="check_completion_percentage",
        ),
        CheckConstraint(
            "effectiveness_rating BETWEEN 1 AND 10", name="check_effectiveness_rating"
        ),
        Index("idx_user_feedback", "user_id", "plan_id"),
    )
