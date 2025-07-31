"""
Enum data types for models. It's better to have all the enums here for better maintainability and to prevent change
"""

from enum import Enum


# for users
class UserRole(str, Enum):
    user = "user"
    coach = "coach"  # Can view and edit fitness exercises
    admin = "admin"


# for profile
class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    unspecified = "unspecified"


class FitnessLevelEnum(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class PrimaryGoalEnum(str, Enum):
    lose_weight = "lose_weight"
    build_muscle = "build_muscle"
    maintain_health = "maintain_health"
    improve_endurance = "improve_endurance"


# exercises


class Difficulty(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
