import uuid

from sqlalchemy import (
    JSON,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship

from .base import Base
from .enums import FitnessLevelEnum, GenderEnum, PrimaryGoalEnum


class UserProfile(Base):
    __tablename__ = "profile"
    profile_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    birth_date = Column(Date, nullable=False)
    gender = Column(
        ENUM(GenderEnum, name="gender_enum", create_type=True),
        nullable=False,
        server_default=text(f"'{GenderEnum.unspecified.value}'::gender_enum"),
    )
    height_cm = Column(Numeric(5, 2), nullable=False)
    weight_kg = Column(Numeric(5, 2), nullable=False)
    fitness_level = Column(
        ENUM(FitnessLevelEnum, name="fitness_enum", create_type=True),
        nullable=False,
        server_default=FitnessLevelEnum.beginner.value,
    )
    primary_goal = Column(
        ENUM(PrimaryGoalEnum, name="primary_goal_enum", create_type=True),
        nullable=False,
        server_default=PrimaryGoalEnum.maintain_health.value,
    )
    medical_conditions = Column(Text, nullable=True)
    preferences = Column(JSON, nullable=True, server_default="{}")
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="profile")
