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


EXPECTED_SCHEMAS = {
    "user_profiles": {
        "profile_id": "UUID",
        "user_id": "UUID",
        "birth_date": "Date",
        "gender": "String",
        "height_cm": "Numeric",
        "weight_kg": "Numeric",
        "fitness_level": "String",
        "primary_goal": "String",
        "medical_conditions": "Text",
        "preferences": "JSON",
        "updated_at": "DateTime",
    },
    "exercises": {
        "exercise_id": "UUID",
        "name": "String",
        "description": "Text",
        "muscle_group": "String",
        "equipment_required": "Array[String]",
        "difficulty": "String",
    },
    "workout_sessions": {
        "session_id": "UUID",
        "user_id": "UUID",
        "start_time": "DateTime",
        "duration_minutes": "Integer",
        "perceived_intensity": "Integer",
        "notes": "Text",
        "session_type": "String",
    },
    "session_exercises": {
        "session_exercise_id": "UUID",
        "session_id": "UUID",
        "exercise_id": "UUID",
        "sets": "Integer",
        "reps": "Integer",
        "weight_kg": "Numeric",
        "distance_km": "Numeric",
        "notes": "Text",
    },
    "workout_plans": {
        "plan_id": "UUID",
        "user_id": "UUID",
        "generated_at": "DateTime",
        "valid_from": "Date",
        "valid_to": "Date",
        "focus_area": "String",
        "ai_model_version": "String",
        "plan_data": "JSON",
    },
    "plan_feedback": {
        "feedback_id": "UUID",
        "plan_id": "UUID",
        "user_id": "UUID",
        "completion_percentage": "Integer",
        "effectiveness_rating": "Integer",
        "created_at": "DateTime",
    },
}
