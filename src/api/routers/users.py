from argon2 import PasswordHasher
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.api.crud.users import create_user_db
from src.api.schemas.v1.users import UserCreate, UserLogin, UserRead
from src.db import get_db

ph = PasswordHasher()

router = APIRouter()


@router.post(
    "/users/sign-up/", status_code=status.HTTP_201_CREATED, response_model=UserRead
)
async def sign_up(create_data: UserCreate, db: Session = Depends(get_db)):
    # TODO: check for duplicated email
    email = create_data.email
    password = ph.hash(create_data.password)
    user = create_user_db(db, email, password)
    return user


@router.post(
    "/users/sign-in/", status_code=status.HTTP_200_OK, response_model=UserLogin
)
async def sign_in(login_data: UserLogin, db: Session = Depends(get_db)):
    pass


# TODO change password
