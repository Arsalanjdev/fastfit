import enum
import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, UUID
from sqlalchemy.orm import relationship

from .base import Base


class Difficulty(str, enum.Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


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
        ENUM(Difficulty, name="difficulty_enum"),
        nullable=False,
        default=Difficulty.BEGINNER,
    )

    session_exercises = relationship("SessionExercises", back_populates="exercise")
