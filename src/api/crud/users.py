from datetime import datetime
from uuid import uuid4

from argon2 import PasswordHasher
from sqlalchemy.orm import Session

from src.api.models.users import User

ph = PasswordHasher()


def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email)
    return user


def create_user_db(db: Session, email: str, password: str, role: str = "user"):
    uuid = uuid4()
    password = ph.hash(password)
    created_at = datetime.now()

    user = User(
        user_id=uuid,
        email=email,
        created_at=created_at,
        is_active=True,
        password=password,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
