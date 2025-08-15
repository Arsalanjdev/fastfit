from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from src.api.crud.users import delete_user_db


def test_integration_authentication_success(db_session: Session, client: TestClient):
    # create user
    email = "email@example.com"
    password = "!AWEHwioe41j250!"
    response = client.post(
        "/v1/users/sign-up", json={"email": email, "password": password}
    )
    assert response.status_code == 201
    assert response.json()["email"] == email

    # authenticating the user
    response = client.post("/token", json={"user_name": email, "password": password})
    data = response.json()
    assert response.status_code == 200
    assert "bearer" in data
    assert "access_token" in data
    assert "user_id" in data

    assert delete_user_db(db_session, email=email)
