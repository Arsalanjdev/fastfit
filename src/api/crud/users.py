from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from src.api.models.users import User


def get_user_by_email(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    return user


def get_user_by_id(db: Session, user_id: UUID) -> User:
    user = db.query(User).filter(User.user_id == user_id).first()
    return user


def create_user_db(db: Session, email: str, password: str, role: str = "user") -> User:
    uuid = uuid4()
    created_at = datetime.now().isoformat()

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


def delete_user_db(
    db: Session, *, user_id: UUID | None = None, email: str | None = None
) -> bool:
    if not user_id and not email:
        raise ValueError("Either user_id or email must be provided.")

    user = None
    if user_id:
        user = get_user_by_id(db, user_id)
    elif email:
        user = get_user_by_email(db, email)

    if not user:
        return False

    db.delete(user)
    db.commit()
    return True
