from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.models.user_profiles import UserProfile
from src.api.models.users import User


def get_profile_by_id(db: Session, id: UUID) -> UserProfile:
    profile = db.query(UserProfile).filter(UserProfile.profile_id == id).first()
    return profile


def get_profile_by_email(db: Session, email: str) -> UserProfile:
    stmt = select(UserProfile).join(User).where(User.email == email)
    return db.execute(stmt).scalars().first()


def update_profile_field(
    db: Session, profile: UserProfile, field_name: str, value
) -> UserProfile:
    if not hasattr(profile, field_name):
        raise AttributeError(f"User Profile doesn't have a {field_name} column.")

    setattr(profile, field_name, value)
    profile.updated_at = datetime.now().isoformat()
    db.commit()
    db.refresh(profile)
    return profile


def delete_profile_from_db(db: Session, profile: UserProfile):
    profile = get_profile_by_id(db, profile.profile_id)
    if not profile:
        return False
    db.delete(profile)
    db.commit()
    return True
