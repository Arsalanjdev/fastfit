import uuid

from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship

from .base import Base
from .enums import UserRole


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    is_active = Column(Boolean, nullable=False, server_default="true")
    password = Column(String(128), nullable=False)
    role = Column(
        ENUM(UserRole, name="user_role_enum"),
        server_default=UserRole.user.value,
        nullable=False,
    )

    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        passive_deletes=True,
        cascade="all, delete-orphan",
    )
    workout_plans = relationship(
        "WorkoutPlans",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    feedback = relationship(
        "PlanFeedback",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"User id {self.user_id} with {self.email}"
