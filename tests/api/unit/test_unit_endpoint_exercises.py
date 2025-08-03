import httpx

from tests.factories.models import get_random_exercise_dict


def test_unit_endpoint_exercises_get_exercise(client: httpx.Client, monkeypatch):
    exercise = get_random_exercise_dict()

    def get_exercise_by_id(*args, **kwargs):
        return exercise

    monkeypatch.setattr(
        "src.api.routers.exercises.get_exercise_by_id", get_exercise_by_id
    )

    exercise_id = exercise["exercise_id"]
    response = client.get(f"/v1/exercises/{exercise_id}/")
    assert response.status_code == 200
