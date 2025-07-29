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
    """
    Generate a randomized password string of exactly 8 characters.

    The password will always include at least one uppercase letter,
    one lowercase letter, one digit, and one special character
    (punctuation or currency symbol). The remaining characters are
    randomly chosen from a broad set excluding whitespace control
    characters.

    Returns:
        str: A shuffled 8-character password meeting the above criteria.
    """
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


@given(email=st.emails(), is_active=st.booleans(), created_at=st.datetimes())
def test_schema_users_read(email: str, is_active: bool, created_at: datetime):
    valid_data = {
        "email": email,
        "is_active": is_active,
        "created_at": created_at,
    }
    read_user = UserRead(**valid_data)
    assert read_user.email == EmailValidator.validate_python(email)
    assert read_user.is_active == is_active
    assert read_user.created_at == created_at


def test_user_read_invalid_email():
    with pytest.raises(ValidationError):
        UserRead(email="not-an-email", is_active=True, created_at=datetime.now())


@given(email=st.emails(), password=passwords())
def test_schema_users_create(email: str, password: str):
    valid_data = {"email": email, "password": password}
    user_created = UserCreate(**valid_data)

    assert user_created.email == EmailValidator.validate_python(email)
    assert user_created.password == password


@pytest.mark.parametrize(
    "bad_password",
    [
        "hello"  # short password,
        "alllowercase1!",  # no uppercase
        "ALLUPPERCASE1!",  # no lowercase
        "NoDigits!!!",  # no digits
        "NoSpecial123",  # no special chars
        # TODO: check against common passwords
    ],
)
def test_schema_users_create_bad_password(bad_password):
    with pytest.raises(ValidationError):
        UserCreate(email="example@example.com", password=bad_password)
