"""add temporary login lockout

Revision ID: g4b9c6e3d825
Revises: f3a8b5d2c714
Create Date: 2026-08-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "g4b9c6e3d825"
down_revision: Union[str, None] = "f3a8b5d2c714"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column(
                "failed_login_attempts",
                sa.Integer(),
                server_default="0",
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "locked_until",
                sa.DateTime(timezone=True),
                nullable=True,
            )
        )

    with op.batch_alter_table("login_audit_logs") as batch_op:
        batch_op.drop_constraint(
            "authfailurereason", type_="check"
        )
        batch_op.create_check_constraint(
            "authfailurereason",
            "failure_reason IN ('INVALID_CREDENTIALS', 'ACCOUNT_BLOCKED', "
            "'TEMPORARILY_LOCKED', 'ROLE_NOT_ALLOWED')",
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
                "key": "failed_login_attempt_limit",
                "value": "3",
                "description": (
                    "Consecutive invalid-password attempts allowed before a "
                    "20-minute temporary account lock."
                ),
            }
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "DELETE FROM system_settings "
            "WHERE key = 'failed_login_attempt_limit'"
        )
    )
    op.execute(
        sa.text(
            "UPDATE login_audit_logs SET failure_reason = 'ACCOUNT_BLOCKED' "
            "WHERE failure_reason = 'TEMPORARILY_LOCKED'"
        )
    )
    with op.batch_alter_table("login_audit_logs") as batch_op:
        batch_op.drop_constraint("authfailurereason", type_="check")
        batch_op.create_check_constraint(
            "authfailurereason",
            "failure_reason IN ('INVALID_CREDENTIALS', 'ACCOUNT_BLOCKED', "
            "'ROLE_NOT_ALLOWED')",
        )
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("locked_until")
        batch_op.drop_column("failed_login_attempts")
