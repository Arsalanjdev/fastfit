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

from hypothesis import given
from hypothesis import strategies as st

from src.api.schemas.v1.workout_plans import WorkoutPlansCreate

simple_json_dict = st.dictionaries(
    keys=st.text(min_size=1, max_size=20),
    values=st.text(min_size=1, max_size=100),
    min_size=1,
    max_size=10,
)


@given(
    valid_from=st.dates(),
    valid_to=st.dates(),
    focus_area=st.text(min_size=3, max_size=50),
    ai_model_version=st.text(min_size=3, max_size=50),
    plan_data=simple_json_dict,
)
def test_schema_create_workout_plan(
    valid_from, valid_to, focus_area, ai_model_version, plan_data
):
    dummy_plan = {
        "valid_from": valid_from,
        "valid_to": valid_to,
        "focus_area": focus_area,
        "ai_model_version": ai_model_version,
        "plan_data": plan_data,
    }
    workout_read = WorkoutPlansCreate(**dummy_plan)
    assert workout_read.valid_from == valid_from
    assert workout_read.valid_to == valid_to
    assert workout_read.focus_area == focus_area
    assert workout_read.ai_model_version == ai_model_version
    assert workout_read.plan_data == plan_data
