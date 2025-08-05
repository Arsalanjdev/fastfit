import pytest
from fastapi import HTTPException

from src.api.crud.users import delete_user_db


def test_integration_users_signup_duplicated_email(db_session, client):
    """
    Tests the endpoint rejects the duplicate email sign up.
    :param client:
    :return:
    """
    # signing up the first user
    email = "email@example.com"
    password = "!AWEHwioe41j250!"
    response = client.post(
        "/v1/users/sign-up", json={"email": email, "password": password}
    )
    assert response.status_code == 201
    assert response.json()["email"] == email

    # trying to sign up the second user
    with pytest.raises(HTTPException):
        client.post("/v1/users/sign-up", json={"email": email, "password": password})

    # cleaning up
    delete_user_db(db_session, email=email)
