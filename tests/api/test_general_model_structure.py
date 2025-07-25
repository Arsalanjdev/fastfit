"""
Tests the general structure checks for all models.
"""

from pytest import mark

# from .fixtures import db_inspect


EXPECTED_TABLES = [
    "users",
    "profile",
    "exercises",
    "workout_sessions",
    "session_exercises",
    "workout_plans",
    "plan_feedback",
]


@mark.parametrize("table_name", EXPECTED_TABLES)
def test_model_table_exists(db_inspect, table_name):
    assert db_inspect.has_table(table_name)


EXPECTED_SCHEMAS = {
    "users": {
        "user_id": "UUID",
        "email": "String",
        "created_at": "DateTime",
        "is_active": "Boolean",
    },
    "profile": {
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


@mark.parametrize(
    "table,column,expected_type",
    [
        (table, col, expected)
        for table, cols in EXPECTED_SCHEMAS.items()
        for col, expected in cols.items()
    ],
)
def test_model_column_data_types(db_inspect, table, column, expected_type):
    from sqlalchemy import (
        ARRAY,
        JSON,
        Boolean,
        Date,
        DateTime,
        Integer,
        Numeric,
        String,
        Text,
    )
    from sqlalchemy.dialects.postgresql import UUID

    TYPE_MAPPING = {
        "UUID": UUID,
        "String": String,
        "Integer": Integer,
        "Boolean": Boolean,
        "DateTime": DateTime,
        "Date": Date,
        "Text": Text,
        "JSON": JSON,
        "Numeric": Numeric,
        "Array[String]": ARRAY,  # special handling below
    }

    expected_cls = TYPE_MAPPING[expected_type]

    columns = db_inspect.get_columns(table)
    col_map = {col["name"]: col["type"] for col in columns}
    actual = col_map.get(column)

    if expected_type == "Array[String]":
        assert isinstance(
            actual, ARRAY
        ), f"{table}.{column} expected ARRAY, got {actual}"
        from sqlalchemy import String

        assert isinstance(
            actual.item_type, String
        ), f"{table}.{column} expected ARRAY[String], got ARRAY[{type(actual.item_type)}]"
    else:
        assert isinstance(
            actual, expected_cls
        ), f"{table}.{column} expected {expected_cls}, got {actual}"

    assert isinstance(
        actual, expected_cls
    ), f"{table}.{column} expected {expected_cls}, got {actual}"


EXPECTED_NULLABLE = {
    "users": {
        "user_id": False,
        "email": False,
        "created_at": False,
        "is_active": False,
    },
    "profile": {
        "profile_id": False,
        "user_id": False,
        "birth_date": False,
        "gender": False,
        "height_cm": False,
        "weight_kg": False,
        "fitness_level": False,
        "primary_goal": False,
        "medical_conditions": True,
        "preferences": True,
        "updated_at": False,
    },
    "exercises": {
        "exercise_id": False,
        "name": False,
        "description": True,
        "muscle_group": False,
        "equipment_required": True,
        "difficulty": False,
    },
    "workout_sessions": {
        "session_id": False,
        "user_id": False,
        "start_time": True,
        "duration_minutes": True,
        "perceived_intensity": True,
        "notes": True,
        "session_type": True,
    },
    "session_exercises": {
        "session_exercise_id": False,
        "session_id": False,
        "exercise_id": False,
        "sets": True,
        "reps": True,
        "weight_kg": True,
        "distance_km": True,
        "notes": True,
    },
    "workout_plans": {
        "plan_id": False,
        "user_id": False,
        "generated_at": False,
        "valid_from": True,
        "valid_to": True,
        "focus_area": True,
        "ai_model_version": False,
        "plan_data": False,
    },
    "plan_feedback": {
        "feedback_id": False,
        "plan_id": False,
        "user_id": False,
        "completion_percentage": False,
        "effectiveness_rating": True,
        "created_at": False,
    },
}


@mark.parametrize(
    "table,column,expected_nullable",
    [
        (table, column, expected_null)
        for table, columns in EXPECTED_NULLABLE.items()
        for column, expected_null in columns.items()
    ],
)
def test_model_column_nullable(db_inspect, table, column, expected_nullable):
    columns = db_inspect.get_columns(table)
    col_map = {column["name"]: column["nullable"] for column in columns}
    actual = col_map.get(column)
    assert actual == expected_nullable


EXPECTED_CONSTRAINTS = {
    "workout_sessions": [
        "check_perceived_intensity_range",
    ],
    "plan_feedback": ["check_completion_percentage", "check_effectiveness_rating"],
}


@mark.parametrize(
    "table,constraint_name",
    [
        (table, constraint)
        for table, constraints in EXPECTED_CONSTRAINTS.items()
        for constraint in constraints
    ],
)
def test_model_check_constraints_exist(db_inspect, table, constraint_name):
    column_checks = db_inspect.get_check_constraints(table)
    check_list = [chk["name"] for chk in column_checks]
    assert constraint_name in check_list


#
# EXPECTED_DEFAULT = {
#     "users": {
#         "user_id": False,
#         "email": False,
#         "created_at": True,  # default=now()
#         "is_active": True,  # default=True
#     },
#     "profile": {
#         "profile_id": False,
#         "user_id": False,
#         "birth_date": False,
#         "gender": True,  # optionally default to 'unspecified' or similar
#         "height_cm": False,
#         "weight_kg": False,
#         "fitness_level": True,  # default e.g. 'beginner'
#         "primary_goal": True,  # default e.g. 'general_fitness'
#         "medical_conditions": False,
#         "preferences": True,
#         "updated_at": True,
#     },
#     "exercises": {
#         "exercise_id": False,
#         "name": False,  # required
#         "description": False,
#         "muscle_group": False,  # required
#         "equipment_required": True,  # default=None or empty
#         "difficulty": True,
#     },
#     "workout_sessions": {
#         "session_id": True,  # auto-increment
#         "user_id": False,  # required FK
#         "start_time": True,  # default=now()
#         "duration_minutes": False,  # user-entered
#         "perceived_intensity": True,  # default e.g. 5
#         "notes": True,  # default empty
#         "session_type": True,  # default e.g. 'custom'
#     },
#     "session_exercises": {
#         "session_exercise_id": True,  # auto-increment
#         "session_id": False,  # required FK
#         "exercise_id": False,  # required FK
#         "sets": True,  # default=3
#         "reps": True,  # default=10
#         "weight_kg": True,  # default=0.0
#         "distance_km": True,  # default=0.0
#         "notes": True,  # default empty
#     },
#     "workout_plans": {
#         "plan_id": True,  # auto-increment
#         "user_id": False,  # required
#         "generated_at": True,  # default=now()
#         "valid_from": True,  # default=now()
#         "valid_to": True,  # default=now() + 1 week
#         "focus_area": True,  # default e.g. 'full_body'
#         "ai_model_version": True,  # default current version
#         "plan_data": False,  # large data; must be filled by system
#     },
#     "plan_feedback": {
#         "feedback_id": False,  # auto-increment
#         "plan_id": False,  # required
#         "user_id": False,  # required
#         "completion_percentage": True,  # default=0
#         "effectiveness_rating": True,  # default=0 or null
#         "created_at": True,  # default=now()
#     },
# }
#
#
# @mark.parametrize(
#     "table,column,expected_default",
#     [
#         (table, column, expected_default)
#         for table, columns in EXPECTED_DEFAULT.items()
#         for column, expected_default in columns.items()
#     ],
# )
# def test_model_default_value_exist(db_inspect, table, column, expected_default):
#     columns = db_inspect.get_columns(table)
#     col_map = {colx["name"]: colx["default"] for colx in columns}
#     actual = col_map.get(column)
#     # for col in columns:
#     #     print(f"  {col['name']}: default={col['default']}")
#     engine = db_inspect.bind
#     with engine.connect() as conn:
#         result = conn.execute(text(f"""
#             SELECT column_default
#             FROM information_schema.columns
#             WHERE table_name = 'plan_feedback'
#             AND column_name = 'completion_percentage'
#         """))
#         print("DB DEFAULT:", result.scalar())
#     col = next((c for c in columns if c['name'] == column), None)
#     has_default = col is not None and col.get('default') is not None
#     assert has_default == expected_default


EXPECTED_COLUMN_LENGTHS: dict[str, dict[str, int]] = {
    "users": {
        "email": 255,
    },
    "profile": {},
    "exercises": {
        "name": 100,
        "muscle_group": 50,
    },
    "workout_sessions": {},
    "workout_plans": {
        "focus_area": 50,
        "ai_model_version": 50,
    },
}


@mark.parametrize(
    "table,column,expected_length",
    [
        (table, column, expected_length)
        for table, cols in EXPECTED_COLUMN_LENGTHS.items()
        for column, expected_length in cols.items()
    ],
)
def test_model_column_length(db_inspect, table, column, expected_length):
    columns = db_inspect.get_columns(table)
    col = next((c for c in columns if c["name"] == column), None)

    # Verify column exists
    assert col is not None, f"Column {column} not found in table {table}"

    # Get the type object
    col_type = col["type"]

    # Verify it's a string type with length attribute
    assert hasattr(
        col_type, "length"
    ), f"Column {table}.{column} is not a string type (has no length)"

    # Verify the length matches
    assert (
        col_type.length == expected_length
    ), f"Length mismatch for {table}.{column}: expected {expected_length}, got {col_type.length}"


# Multiple columns constraints
EXPECTED_UNIQUE_CONSTRAINTS = {
    "workout_sessions": [
        "uq_user_session_time",
    ],
    "plan_feedback": [
        "uq_feedback_per_plan_user",
    ],
    "session_exercises": [
        "uq_session_exercise",
    ],
    "workout_plans": [
        "uq_user_plan_dates",
    ],
}


@mark.parametrize(
    "table,constraint_name",
    [
        (table, name)
        for table, names in EXPECTED_UNIQUE_CONSTRAINTS.items()
        for name in names
    ],
)
def test_model_unique_constraint_exists(db_inspect, table, constraint_name):
    uniques = db_inspect.get_unique_constraints(table)
    unique_names = {uc["name"] for uc in uniques}
    assert (
        constraint_name in unique_names
    ), f"Unique constraint '{constraint_name}' not found in table '{table}'"
