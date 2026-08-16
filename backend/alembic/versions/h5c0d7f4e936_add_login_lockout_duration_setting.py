"""add login lockout duration setting

Revision ID: h5c0d7f4e936
Revises: g4b9c6e3d825
Create Date: 2026-08-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "h5c0d7f4e936"
down_revision: Union[str, None] = "g4b9c6e3d825"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            "system_settings",
            sa.column("key", sa.String()),
            sa.column("value", sa.String()),
            sa.column("description", sa.String()),
        ),
        [
            {
                "key": "login_lockout_duration_minutes",
                "value": "20",
                "description": (
                    "Minutes an account remains temporarily locked after too "
                    "many failed login attempts."
                ),
            }
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "DELETE FROM system_settings "
            "WHERE key = 'login_lockout_duration_minutes'"
        )
    )
