from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: Annotated[EmailStr, Field(description="User email")]
    is_active: Annotated[bool, Field(description="Is the user active?")]


class UserRead(UserBase):
    pass
