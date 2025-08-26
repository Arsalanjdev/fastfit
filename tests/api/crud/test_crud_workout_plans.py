import uuid
from datetime import date, timedelta

import pytest
from sqlalchemy.orm import Session

from src import User, WorkoutPlans
from src.api.crud.users import create_user_with_profile, delete_user_db
from src.api.crud.workout_plans import (
    create_workout_plan_db,
    get_workout_plans_by_user_id,
)
from src.api.models.enums import FitnessLevelEnum, GenderEnum, PrimaryGoalEnum
from tests.utils import is_valid_uuid

# plan_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
# user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
# generated_at = Column(DateTime, server_default=func.now(), nullable=False)
# valid_from = Column(Date, nullable=True)
# valid_to = Column(Date, nullable=True)
# focus_area = Column(String(50), nullable=True)
# ai_model_version = Column(String(50), nullable=False)
# plan_data = Column(JSON, nullable=False)

#
# def create_user(
#     db: Session,
#     email="example@mail.com",
#     password="example@mail.com",
#     birthdate: date = date(1970, 1, 1),
#     delete_all_users=True,
# ):
#     if delete_all_users:
#         db.query(User).delete(synchronize_session=False)
#         db.commit()
#     created_user, created_profile = create_user_with_profile(
#         email=email, password=password, birth_date=birthdate
#     )
#     yield created_user, created_profile
#     delete_user_db(created_user)


def test_create_workout_plan(db_session, user_factory):
    email = "doawhdi@gmail.com"
    user, profile = user_factory(email=email)
    user_id = user.user_id
    plan = {
        "user_id": user_id,
        "valid_from": date.today(),
        "valid_to": date.today(),
        "focus_area": "General",
        "ai_model_version": "deepseekv1",
        "plan_data": {
            "plank": 20,
        },
    }
    workout_plan_db = create_workout_plan_db(db_session, **plan)

    assert is_valid_uuid(workout_plan_db.plan_id)
    assert workout_plan_db.user_id == user_id
    assert workout_plan_db.valid_from == plan["valid_from"]
    assert workout_plan_db.valid_to == plan["valid_to"]
    assert workout_plan_db.focus_area == plan["focus_area"]
    assert workout_plan_db.ai_model_version == plan["ai_model_version"]
    assert workout_plan_db.plan_data == plan["plan_data"]

    second_plan = plan.copy()
    second_plan["valid_to"] = date.today() + timedelta(days=1)
    second_plan["focus_area"] = "Legs"
    workout_plan_db_2 = create_workout_plan_db(db_session, **second_plan)
    assert workout_plan_db_2.plan_id != workout_plan_db.plan_id

    assert len(user.workout_plans) == 2
    assert workout_plan_db.user == user
    assert workout_plan_db in user.workout_plans


def test_read_get_all_workout_plan_by_user(db_session, user_factory):
    user, profile = user_factory()
    plan = {
        "user_id": user.user_id,
        "valid_from": date.today(),
        "valid_to": date.today(),
        "focus_area": "General",
        "ai_model_version": "deepseekv1",
        "plan_data": {
            "plank": 20,
        },
    }
    plan_2 = {
        "user_id": user.user_id,
        "valid_from": date.today() + timedelta(days=1),
        "valid_to": date.today() + timedelta(days=2),
        "focus_area": "Legs",
        "ai_model_version": "deepseekv1",
        "plan_data": {
            "walk": 30,
        },
    }
    create_workout_plan_db(db_session, **plan)
    create_workout_plan_db(db_session, **plan_2)

    plans = get_workout_plans_by_user_id(db_session, user.user_id)
    assert len(plans) == 2
