import uuid
from datetime import datetime

import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.strategies import characters, composite, text
from pydantic import EmailStr, TypeAdapter, ValidationError

from src.api.schemas.v1.users import UserCreate, UserRead

EmailValidator = TypeAdapter(EmailStr)


@composite
def passwords(draw):
    uppercase = characters(whitelist_categories=["Lu"])
    lowercase = characters(whitelist_categories=["Ll"])
    digits = characters(whitelist_categories=["Nd"])
    special = characters(whitelist_categories=["Po", "Sc"])
    uppercase_char = draw(uppercase)
    lowercase_char = draw(lowercase)
    digit_char = draw(digits)
    special_char = draw(special)

    others = draw(
        text(
            characters(blacklist_characters=["\n", "\r", "\t", "\x0b", "\x0c"]),
            min_size=4,
            max_size=4,
        )
    )

    password_list = list(
        uppercase_char + lowercase_char + digit_char + special_char + others
    )
    rng = draw(st.randoms())
    rng.shuffle(password_list)
    return "".join(password_list)


@given(
    user_id=st.uuids(),
    email=st.emails(),
    is_active=st.booleans(),
    created_at=st.datetimes(),
)
def test_schema_users_read(
    user_id: uuid.UUID, email: str, is_active: bool, created_at: datetime
):
    valid_data = {
        "user_id": user_id,
        "email": email,
        "is_active": is_active,
        "created_at": created_at,
    }
    read_user = UserRead(**valid_data)
    assert read_user.user_id == user_id
    assert read_user.email == EmailValidator.validate_python(email)
    assert read_user.is_active == is_active
    assert read_user.created_at == created_at


def test_user_read_invalid_email():
    with pytest.raises(ValidationError):
        UserRead(
            user_id=uuid.uuid4(),
            email="not-an-email",
            is_active=True,
            created_at=datetime.now(),
        )


@given(email=st.emails(), password=passwords())
def test_schema_users_create(email: str, password: str):
    valid_data = {"email": email, "password": password}
    user_created = UserCreate(**valid_data)
    assert user_created.email == EmailValidator.validate_python(email.lower())
    assert user_created.password == password


@pytest.mark.parametrize(
    "bad_password",
    [
        "hello",  # short password
        "alllowercase1!",  # no uppercase
        "ALLUPPERCASE1!",  # no lowercase
        "NoDigits!!!",  # no digits
        "NoSpecial123",  # no special chars
        "      1A!",  # whitespace (optional: your logic might allow/disallow)
    ],
)
def test_schema_users_create_bad_password(bad_password):
    with pytest.raises(ValidationError):
        UserCreate(email="example@example.com", password=bad_password)


def test_user_create_missing_email():
    with pytest.raises(ValidationError):
        UserCreate(password="Valid123!")


def test_user_create_missing_password():
    with pytest.raises(ValidationError):
        UserCreate(email="test@example.com")


def test_email_normalization():
    user = UserCreate(email="Test@Example.COM", password="Valid123!")
    assert user.email == "test@example.com"


def test_user_read_dict_roundtrip():
    user = UserRead(
        user_id=uuid.uuid4(),
        email="test@example.com",
        is_active=True,
        created_at=datetime.now(),
    )
    user_dict = user.model_dump()
    user2 = UserRead(**user_dict)
    assert user == user2


@pytest.mark.parametrize(
    "length,should_pass",
    [
        (7, False),  # below minimum
        (8, True),  # exact minimum
        (64, True),  # reasonable upper bound
        (128, True),  # very long password
    ],
)
def test_password_length_boundaries(length, should_pass):
    password = "A" * (length - 3) + "a1!"  # ensure other requirements met
    if should_pass:
        UserCreate(email="test@example.com", password=password)
    else:
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com", password=password)


def test_timezone_aware_datetime():
    from datetime import timezone

    tz_aware = datetime.now(timezone.utc)
    user = UserRead(
        user_id=uuid.uuid4(),
        email="test@example.com",
        is_active=True,
        created_at=tz_aware,
    )
    assert user.created_at == tz_aware


def test_invalid_field_types():
    with pytest.raises(ValidationError):
        UserRead(
            user_id="not-a-uuid", email=123, is_active="yes", created_at="not a date"
        )

    with pytest.raises(ValidationError):
        UserCreate(email=123, password=12345678)


def test_case_sensitive_email_handling():
    user1 = UserCreate(email="TEST@example.com", password="Valid123!")
    user2 = UserCreate(email="test@EXAMPLE.com", password="Valid123!")
    assert user1.email == user2.email


def test_json_serialization():
    user = UserRead(
        user_id=uuid.uuid4(),
        email="test@example.com",
        is_active=True,
        created_at=datetime(2023, 1, 1, 12, 0),
    )
    json_str = user.model_dump_json()
    user2 = UserRead.model_validate_json(json_str)
    assert user == user2
