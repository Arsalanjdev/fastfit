from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from src.api.models.user_profiles import UserProfile
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


def create_profile_given_user(
    db: Session,
    user: User,
    birth_date: date,
    height_cm: Decimal,
    weight_kg: Decimal,
    fitness_level: str,
    primary_goal: str,
    gender: str = "unspecified",
    medical_conditions: str | None = None,
    preferences: dict[str, Any] | None = None,
) -> UserProfile:
    preferences = preferences or {}
    user_id = user.user_id
    updated_at = datetime.now().isoformat()
    profile = UserProfile(
        user_id=user_id,
        birth_date=birth_date,
        height_cm=height_cm,
        weight_kg=weight_kg,
        fitness_level=fitness_level,
        primary_goal=primary_goal,
        gender=gender,
        medical_conditions=medical_conditions,
        preferences=preferences,
        updated_at=updated_at,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    db.refresh(user)
    return profile


def create_user_with_profile(
    db: Session,
    *,
    email: str,
    password: str,
    birth_date: date,
    height_cm: Decimal,
    weight_kg: Decimal,
    fitness_level: str,
    primary_goal: str,
    gender: str = "unspecified",
    medical_conditions: str | None = None,
    preferences: dict[str, Any] | None = None,
) -> tuple[User, UserProfile]:
    preferences = preferences or {}
    user = create_user_db(db, email, password)
    profile = create_profile_given_user(
        db=db,
        user=user,
        birth_date=birth_date,
        height_cm=height_cm,
        weight_kg=weight_kg,
        fitness_level=fitness_level,
        primary_goal=primary_goal,
        gender=gender,
        medical_conditions=medical_conditions,
        preferences=preferences,
    )
    return user, profile
