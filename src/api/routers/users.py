from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.api.crud.users import create_user_db
from src.api.schemas.v1.users import UserCreate, UserRead
from src.db import get_db

router = APIRouter()


@router.post(
    "/users/sign-up/", status_code=status.HTTP_201_CREATED, response_model=UserRead
)
async def sign_up(create_data: UserCreate, db: Session = Depends(get_db)):
    email = create_data.email
    password = create_data.password
    user = create_user_db(db, email, password)
    return user
