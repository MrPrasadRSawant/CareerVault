"""add system settings and daily registration limit

Revision ID: f3a8b5d2c714
Revises: e2f7a4c9d631
Create Date: 2026-08-16
"""

from datetime import date
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f3a8b5d2c714"
down_revision: Union[str, None] = "e2f7a4c9d631"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "system_settings",
        sa.Column("key", sa.String(length=100), nullable=False),
        sa.Column("value", sa.String(length=500), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("updated_by", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(
            ["updated_by"], ["users.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("key"),
    )
    op.create_table(
        "daily_registration_counters",
        sa.Column("registration_date", sa.Date(), nullable=False),
        sa.Column("registration_count", sa.Integer(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "registration_count >= 0",
            name=op.f(
                "ck_daily_registration_counters_registration_count_non_negative"
            ),
        ),
        sa.PrimaryKeyConstraint("registration_date"),
    )
    connection = op.get_bind()
    users = sa.table(
        "users",
        sa.column("created_at", sa.DateTime()),
        sa.column("role", sa.String()),
    )
    registration_day = sa.func.date(users.c.created_at)
    existing_counts = connection.execute(
        sa.select(registration_day, sa.func.count())
        .where(users.c.role == "JOB_APPLICANT")
        .group_by(registration_day)
    ).all()
    if existing_counts:
        counters = sa.table(
            "daily_registration_counters",
            sa.column("registration_date", sa.Date()),
            sa.column("registration_count", sa.Integer()),
        )
        op.bulk_insert(
            counters,
            [
                {
                    "registration_date": (
                        date.fromisoformat(day) if isinstance(day, str) else day
                    ),
                    "registration_count": count,
                }
                for day, count in existing_counts
            ],
        )
    op.bulk_insert(
        sa.table(
            "system_settings",
            sa.column("key", sa.String()),
            sa.column("value", sa.String()),
            sa.column("description", sa.String()),
        ),
        [
            {
                "key": "daily_registration_limit",
                "value": "1000",
                "description": (
                    "Maximum number of public account registrations allowed "
                    "per UTC day."
                ),
            }
        ],
    )


def downgrade() -> None:
    op.drop_table("daily_registration_counters")
    op.drop_table("system_settings")
