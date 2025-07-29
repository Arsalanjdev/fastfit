"""user role added

Revision ID: 10c65c40427f
Revises: 7f2b1c96f698
Create Date: 2025-07-29 08:33:52.021926

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "10c65c40427f"
down_revision: Union[str, Sequence[str], None] = "7f2b1c96f698"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create the enum type in the database
    op.execute("CREATE TYPE user_role_enum AS ENUM ('user', 'coach', 'admin')")
    # 2. Add the column with the enum type and default value (use sa.text for default)
    op.add_column(
        "users",
        sa.Column(
            "role",
            postgresql.ENUM("user", "coach", "admin", name="user_role_enum"),
            server_default=sa.text("'user'"),
            nullable=False,
        ),
    )
    op.execute("UPDATE users SET role='user' WHERE role IS NULL")


def downgrade() -> None:
    # Drop the column first
    op.drop_column("users", "role")
    # Then drop the enum type
    op.execute("DROP TYPE user_role_enum")
