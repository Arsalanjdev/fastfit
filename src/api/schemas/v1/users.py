from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserAuthBase(BaseModel):
    email: Annotated[EmailStr, Field(description="User email")]
    password: Annotated[str, Field(description="User password")]

    @field_validator("email")
    def email_normalization(cls, v: str):
        return v.lower()


class UserRead(BaseModel):
    email: Annotated[EmailStr, Field(description="User email")]
    created_at: Annotated[
        datetime, Field(description="Data time of when user was created.")
    ]
    is_active: Annotated[bool, Field(description="Is the user active?")]

    class Config:
        orm_mode = True


class UserCreate(UserAuthBase):
    password: Annotated[str, Field(description="Password of the user")]

    @field_validator("password")
    def password_complexity(cls, password: str):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must have at least one uppercase letter")
        if not any(c.islower() for c in password):
            raise ValueError("Password must have at least one lowercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must have at least one digit")
        if not any(not c.isalnum() for c in password):
            raise ValueError("Password must have at least one special character")

        return password


class UserUpdate(BaseModel):
    email: Annotated[Optional[EmailStr], Field(description="User email")]
    password: Annotated[Optional[str], Field(description="User password")]
    is_active: Annotated[
        Optional[bool], Field(description="Toggle the activation of the user")
    ]  # TODO: for admins


class UserLogin(UserAuthBase):
    pass
