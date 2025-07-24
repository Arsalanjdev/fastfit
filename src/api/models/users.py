import uuid

from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    is_active = Column(Boolean, nullable=False, server_default="true")

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    workout_plans = relationship(
        "WorkoutPlans", back_populates="user", cascade="all, delete-orphan"
    )
    feedback = relationship(
        "PlanFeedback", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User id {self.id} with {self.email}"
