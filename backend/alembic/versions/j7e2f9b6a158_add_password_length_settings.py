"""add password length settings

Revision ID: j7e2f9b6a158
Revises: i6d1e8a5f047
Create Date: 2026-08-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "j7e2f9b6a158"
down_revision: Union[str, None] = "i6d1e8a5f047"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    settings_table = sa.table(
        "system_settings",
        sa.column("key", sa.String()),
        sa.column("value", sa.String()),
        sa.column("description", sa.String()),
    )
    op.bulk_insert(
        settings_table,
        [
            {
                "key": "password_min_length",
                "value": "8",
                "description": "Minimum accepted password character length.",
            },
            {
                "key": "password_max_length",
                "value": "20",
                "description": "Maximum accepted password character length.",
            },
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "DELETE FROM system_settings WHERE key IN "
            "('password_min_length', 'password_max_length')"
        )
    )
