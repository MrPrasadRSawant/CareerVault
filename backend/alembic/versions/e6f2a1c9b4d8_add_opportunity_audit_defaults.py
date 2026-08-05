"""add database defaults for opportunity audit timestamps

Revision ID: e6f2a1c9b4d8
Revises: d5e91f7a2b30
Create Date: 2026-08-06
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e6f2a1c9b4d8"
down_revision: Union[str, None] = "d5e91f7a2b30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("job_opportunities", schema=None) as batch_op:
        batch_op.alter_column(
            "created_on_utc",
            existing_type=sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "updated_on_utc",
            existing_type=sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            existing_nullable=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("job_opportunities", schema=None) as batch_op:
        batch_op.alter_column(
            "created_on_utc",
            existing_type=sa.DateTime(timezone=True),
            server_default=None,
            existing_nullable=False,
        )
        batch_op.alter_column(
            "updated_on_utc",
            existing_type=sa.DateTime(timezone=True),
            server_default=None,
            existing_nullable=False,
        )
