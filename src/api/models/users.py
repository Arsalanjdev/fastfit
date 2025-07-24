from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class users(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
