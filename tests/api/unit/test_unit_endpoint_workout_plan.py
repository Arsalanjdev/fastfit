import uuid
from datetime import date
from typing import Any
from uuid import UUID

import httpx


# plan_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
#     generated_at = Column(DateTime, server_default=func.now(), nullable=False)
#     valid_from = Column(Date, nullable=True)
#     valid_to = Column(Date, nullable=True)
#     focus_area = Column(String(50), nullable=True)
#     ai_model_version = Column(String(50), nullable=False)
#     plan_data = Column(JSON, nullable=False)
#
#     user = relationship("User", back_populates="workout_plans")
#     feedback = relationship(
#         "PlanFeedback", back_populates="feedback_plan", cascade="all, delete-orphan"
#     )
def dummy_plan() -> dict[str, Any]:
    return {
        "plan_id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),
        "generated_at": date.today().isoformat(),
        "valid_from": date.today().isoformat(),
        "valid_to": date.today().isoformat(),
        "focus_area": "core",
        "ai_model_version": "deepseekv2",
        "plan_data": {"walking": "walk for 2 hours."},
    }


def test_endpoint_workout_plan_get(client: httpx.Client, monkeypatch) -> None:
    plan = dummy_plan()

    def get_plan(*args, **kwargs) -> dict[str, Any]:
        return plan

    monkeypatch.setattr(
        "src.api.routers.workout_plans.get_workout_plan_by_id", get_plan
    )
    id = plan["plan_id"]
    response = client.get(f"/v1/workout-plans/{id}")

    data = response.json()
    assert isinstance(data, dict)

    assert UUID(data["plan_id"]) == UUID(plan["plan_id"])
    assert data["user_id"] == plan["user_id"]
    assert data["focus_area"] == plan["focus_area"]
    assert data["ai_model_version"] == plan["ai_model_version"]
    assert data["plan_data"] == plan["plan_data"]

    assert response.status_code == 200


def test_endpoint_workout_plan_post(client: httpx.Client, monkeypatch) -> None:
    plan = dummy_plan().copy()

    def create_plan(*args, **kwargs) -> dict[str, Any]:
        return plan

    monkeypatch.setattr(
        "src.api.routers.workout_plans.create_workout_plan_db", create_plan
    )
    dummy_plan().pop("plan_id")
    dummy_plan().pop("user_id")
    dummy_plan().pop("generated_at")
    response = client.post("/v1/workout-plans/create/", json=plan)
    data = response.json()
    assert isinstance(data, dict)
    assert response.status_code == 201
    assert data["plan_id"] == plan["plan_id"]
    assert data["user_id"] == plan["user_id"]
    assert data["generated_at"] == plan["generated_at"]


def test_endpoint_workout_plan_post_invalid_plan(
    client: httpx.Client, monkeypatch
) -> None:
    plan = dummy_plan().copy()

    def create_plan(*args, **kwargs) -> dict[str, Any]:
        return plan

    monkeypatch.setattr(
        "src.api.routers.workout_plans.create_workout_plan_db", create_plan
    )
    plan.pop("plan_data")
    response = client.post("/v1/workout-plans/create/", json=plan)
    assert response.status_code == 422


# def test_endpoint_workout_plan_update(client: httpx.Client, monkeypatch) -> None:
#     plan = dummy_plan().copy()
#
#     def update_plan(*args, **kwargs) -> dict[str, Any]:
#         return plan
#
#     monkeypatch.setattr(
#         "src.api.routers.workout_plans.update_workout_plan_db", update_plan
#     )
