# def test_unit_endpoint_users_create(client: httpx.Client, monkeypatch):
#     random_user = get_random_user_dict()
#
#     def create_user(*args, **kwargs):
#         return {
#             "user": {
#                 "user_id": uuid.uuid4(),
#                 "email": random_user.get("email"),
#                 "created_at": datetime.now().isoformat(),
#                 "is_active": True,
#                 "role": "user",
#             },
#             "profile": {
#                 "birth_date": date(1970, 1, 1),
#                 "gender": GenderEnum.unspecified,
#                 "height_cm": Decimal("175.50"),
#                 "weight_kg": Decimal("70.25"),
#                 "fitness_level": FitnessLevelEnum.intermediate,
#                 "primary_goal": PrimaryGoalEnum.build_muscle,
#                 "medical_conditions": "None",
#                 "preferences": {
#                     "workout_time": "morning",
#                     "preferred_equipment": ["dumbbells", "treadmill"],
#                 },
#                 "profile_id": uuid.uuid4(),
#                 "user_id": uuid.uuid4(),
#                 "updated_at": datetime.now(),
#             },
#         }
#
#     monkeypatch.setattr("src.api.routers.users.create_user_with_profile", create_user)
#
#     create_json = {
#         "user": {
#             "email": random_user.get("email"),
#             "password": random_user.get("key"),
#         },
#         "profile": {
#             "birth_date": date(1970, 1, 1),
#             "gender": GenderEnum.unspecified,
#             "height_cm": Decimal("175.50"),
#             "weight_kg": Decimal("70.25"),
#             "fitness_level": FitnessLevelEnum.intermediate,
#             "primary_goal": PrimaryGoalEnum.build_muscle,
#             "medical_conditions": "None",
#             "preferences": {
#                 "workout_time": "morning",
#                 "preferred_equipment": ["dumbbells", "treadmill"],
#             },
#         },
#     }
#
#     email = "ema313il@example.com"
#     password = "!AWEHwioe41j250!"
#     user = {
#         "email": email,
#         "password": password,
#     }
#     profile = {
#         "birth_date": date(1980, 2, 3).isoformat(),
#         "gender": GenderEnum.male.value,
#         "height_cm": 160,
#         "weight_kg": 50,
#         "fitness_level": FitnessLevelEnum.beginner.value,
#         "primary_goal": PrimaryGoalEnum.maintain_health.value,
#     }
#     body = {
#         "user": user,
#         "profile": profile,
#     }
#
#     response = client.post("/v1/users/sign-up", json=body)
#     response_dict: dict[str, str] = response.json()
#
#     user_id = response_dict["user"]["user_id"]
#     created_at = response_dict["user"]["created_at"]
#
#     assert response.status_code == 201
#     assert user_id is not None and is_valid_uuid(user_id)
#     assert response_dict["user"]["email"] == body["user"]["email"]
#     assert "password" not in response_dict["user"]
#     assert created_at is not None and is_iso_datetime(created_at)
#     assert response_dict["user"]["role"] in ["user", "coach", "admin"]
#     assert response_dict["user"]["is_active"]
#
#
# def test_unit_endpoint_users_signup_missing_email(client):
#     response = client.post("/v1/users/sign-up", json={"password": "dawiooYAR(W*Y%124"})
#     assert response.status_code == 422
#
#
# def test_unit_endpoint_users_signup_missing_password(client):
#     response = client.post("/v1/users/sign-up", json={"email": "mail@example.com"})
#     assert response.status_code == 422
#

#
# def test_unit_endpoint_users_change_password(client):
#     random_user = get_random_user_dict()
#     password = random_user.get("password")
#     email = random_user.get("email")
#
#     def change_password(*args, **kwargs):
#         return {
#             "user_id": uuid.uuid4(),
#             "password": "NewwwwPPPPPas2221",
#             "created_at": datetime.now().isoformat(),
#             "is_active": True,
#             "role": "user"
#         }
#
#     monkeypatch.setattr("src.api.routers.users.change_password_db", change_password)
#     response = client.post(
#         "/v1/users/change-password", json=jsonable_encoder(random_user)
#     )
