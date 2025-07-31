import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, UUID
from sqlalchemy.orm import relationship

from .base import Base
from .enums import DifficultyEnum


class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id = Column(
        UUID(as_uuid=True), nullable=False, default=uuid.uuid4, primary_key=True
    )
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    muscle_group = Column(String(50), nullable=False)
    equipment_required = Column(ARRAY(String(100)), nullable=True)
    difficulty = Column(
        ENUM(DifficultyEnum, name="difficulty_enum"),
        nullable=False,
        default=DifficultyEnum.BEGINNER,
    )

    session_exercises = relationship("SessionExercises", back_populates="exercise")
