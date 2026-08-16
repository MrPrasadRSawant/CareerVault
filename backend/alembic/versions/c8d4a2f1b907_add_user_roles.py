"""add one role per user

Revision ID: c8d4a2f1b907
Revises: b94e2a7c3d51
Create Date: 2026-08-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c8d4a2f1b907"
down_revision: Union[str, None] = "b94e2a7c3d51"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_role = sa.Enum(
        "JOB_APPLICANT",
        "SYSTEM_ADMIN",
        name="userrole",
        native_enum=False,
        length=30,
        create_constraint=True,
    )
    with op.batch_alter_table("users") as batch_op:
        # Earlier migrations used the PostgreSQL-specific `now()` literal.
        # `sa.func.now()` compiles to a portable current-timestamp default so
        # both the documented SQLite setup and PostgreSQL can create users.
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            server_default=sa.func.now(),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(),
            server_default=sa.func.now(),
            existing_nullable=False,
        )
        batch_op.add_column(
            sa.Column(
                "role",
                user_role,
                nullable=False,
                server_default="JOB_APPLICANT",
            )
        )
        batch_op.create_index("ix_users_role", ["role"], unique=False)


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_index("ix_users_role")
        batch_op.drop_column("role")
