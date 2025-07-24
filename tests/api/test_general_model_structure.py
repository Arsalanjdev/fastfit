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
        "fitness_level": True,
        "primary_goal": True,
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
