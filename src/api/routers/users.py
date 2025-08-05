from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.api.crud.users import create_user_with_profile, is_email_duplicated
from src.api.dependencies.db import get_db
from src.api.dependencies.hashing import password_hasher
from src.api.schemas.v1.profiles import UserProfileRead
from src.api.schemas.v1.users import (
    UserCreateWithProfile,
    UserRead,
    UserReadWithProfile,
)

router = APIRouter()


@router.post(
    "/users/sign-up/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserReadWithProfile,
)
async def sign_up(create_data: UserCreateWithProfile, db: Session = Depends(get_db)):
    email = create_data.user.email
    if is_email_duplicated(db, email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Duplicated email. User was not created.",
        )
    password = password_hasher.hash(create_data.user.password)
    create_data_dict = create_data.profile.model_dump()
    user, profile = create_user_with_profile(
        db, email=email, password=password, **create_data_dict
    )
    return {
        "user": UserRead.model_validate(user),
        "profile": UserProfileRead.model_validate(profile),
    }


# TODO change password


# TODO change email
