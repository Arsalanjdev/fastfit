import random
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from faker import Faker

faker = Faker()


@dataclass
class User:
    uuid: UUID
    email: str
    password: str
    is_active: bool
    created_at: datetime
    role: str


def get_random_user_dict(uuid: UUID | None = None):
    if uuid is None:
        uuid = uuid4()
    else:
        uuid = uuid
    dict = {
        "user_id": uuid,
        "email": faker.email(),
        "password": faker.password(),
        "is_active": faker.boolean(),
        "created_at": faker.date_time(),
        "role": random.choice(["user", "coach", "admin"]),
    }
    return dict
