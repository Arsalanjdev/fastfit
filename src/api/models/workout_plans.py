from uuid import uuid4

from sqlalchemy import JSON, Column, Date, DateTime, ForeignKey, Index, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class WorkoutPlans(Base):
    __tablename__ = "workout_plans"

    plan_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    generated_at = Column(DateTime, server_default=func.now(), nullable=False)
    valid_from = Column(Date, nullable=True)
    valid_to = Column(Date, nullable=True)
    focus_area = Column(String, nullable=True)
    ai_model_version = Column(String(255), nullable=False)
    plan_data = Column(JSON, nullable=False)

    user = relationship("User", back_populates="workout_plans")
    feedback = relationship(
        "PlanFeedback", back_populates="workout_plans", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("ix_workout_plans_user_id", "user_id"),)
