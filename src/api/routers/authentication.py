from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.api.crud.users import get_user_by_email
from src.api.dependencies.authentication import create_access_token
from src.api.dependencies.db import get_db
from src.api.dependencies.hashing import password_hasher

router = APIRouter()


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    email = form_data.username
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    password = form_data.password
    if not password_hasher.verify(user.password, password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token({"sub": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.user_id,
    }
