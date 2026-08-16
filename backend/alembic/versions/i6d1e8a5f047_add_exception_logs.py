"""add exception logs

Revision ID: i6d1e8a5f047
Revises: h5c0d7f4e936
Create Date: 2026-08-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "i6d1e8a5f047"
down_revision: Union[str, None] = "h5c0d7f4e936"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "exception_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("request_id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("method", sa.String(length=10), nullable=False),
        sa.Column("route_template", sa.String(length=500), nullable=False),
        sa.Column(
            "query_parameter_names", sa.String(length=1000), nullable=True
        ),
        sa.Column("status_code", sa.Integer(), nullable=False),
        sa.Column("exception_type", sa.String(length=255), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("traceback", sa.Text(), nullable=False),
        sa.Column("fingerprint", sa.String(length=64), nullable=False),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("user_agent", sa.String(length=512), nullable=True),
        sa.Column("app_environment", sa.String(length=50), nullable=False),
        sa.Column(
            "is_handled", sa.Boolean(), server_default="0", nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_exception_logs_request_id",
        "exception_logs",
        ["request_id"],
        unique=True,
    )
    op.create_index(
        "ix_exception_logs_user_id", "exception_logs", ["user_id"]
    )
    op.create_index(
        "ix_exception_logs_occurred_at",
        "exception_logs",
        ["occurred_at"],
    )
    op.create_index(
        "ix_exception_logs_status_code",
        "exception_logs",
        ["status_code"],
    )
    op.create_index(
        "ix_exception_logs_exception_type",
        "exception_logs",
        ["exception_type"],
    )
    op.create_index(
        "ix_exception_logs_fingerprint",
        "exception_logs",
        ["fingerprint"],
    )


def downgrade() -> None:
    op.drop_table("exception_logs")
