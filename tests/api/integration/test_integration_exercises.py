#
# def test_integration_create_exercise_check_the_user_role(
#     db_session: Session, client: TestClient
# ):
#     """
#     Tests that only admin and coaches can create an exercise not ordinary users.
#     :param db_session:
#     :param client:
#     :return:
#     """
#     # signing up
#     email = "email@example.com"
#     password = "!AWEHwioe41j250!"
#     response = client.post(
#         "/v1/users/sign-up", json={"email": email, "password": password}
#     )
#     assert response.status_code == 201
#
#     # authenticating
