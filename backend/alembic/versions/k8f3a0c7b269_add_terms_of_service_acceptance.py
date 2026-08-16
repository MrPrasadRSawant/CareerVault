"""add terms of service settings and acceptance snapshot

Revision ID: k8f3a0c7b269
Revises: j7e2f9b6a158
Create Date: 2026-08-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.repositories.system_setting_repository import (
    DEFAULT_TERMS_OF_SERVICE_CONTENT,
)


revision: str = "k8f3a0c7b269"
down_revision: Union[str, None] = "j7e2f9b6a158"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("system_settings") as batch_op:
        batch_op.alter_column(
            "value",
            existing_type=sa.String(length=500),
            type_=sa.Text(),
            existing_nullable=False,
        )

    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column("terms_accepted_at", sa.DateTime(timezone=True))
        )
        batch_op.add_column(sa.Column("terms_accepted_version", sa.Integer()))
        batch_op.add_column(sa.Column("terms_accepted_content", sa.Text()))

    settings_table = sa.table(
        "system_settings",
        sa.column("key", sa.String()),
        sa.column("value", sa.Text()),
        sa.column("description", sa.String()),
    )
    op.bulk_insert(
        settings_table,
        [
            {
                "key": "terms_of_service_content",
                "value": DEFAULT_TERMS_OF_SERVICE_CONTENT,
                "description": (
                    "Current rich-text Terms of Service shown during account "
                    "registration."
                ),
            },
            {
                "key": "terms_of_service_version",
                "value": "1",
                "description": (
                    "Revision number of the currently published Terms of "
                    "Service."
                ),
            },
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "DELETE FROM system_settings WHERE key IN "
            "('terms_of_service_content', 'terms_of_service_version')"
        )
    )
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("terms_accepted_content")
        batch_op.drop_column("terms_accepted_version")
        batch_op.drop_column("terms_accepted_at")
    with op.batch_alter_table("system_settings") as batch_op:
        batch_op.alter_column(
            "value",
            existing_type=sa.Text(),
            type_=sa.String(length=500),
            existing_nullable=False,
        )
