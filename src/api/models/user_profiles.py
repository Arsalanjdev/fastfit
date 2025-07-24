import uuid

from sqlalchemy import (
    JSON,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class UserProfile(Base):
    __tablename__ = "profile"
    profile_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    height_cm = Column(Numeric(5, 2), nullable=False, default=165)
    weight_kg = Column(Numeric(5, 2), nullable=False, default=80)
    fitness_level = Column(String, nullable=True)
    primary_goal = Column(String, nullable=True)
    medical_conditions = Column(Text, nullable=True)
    preferences = Column(JSON, nullable=True)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="profile")
