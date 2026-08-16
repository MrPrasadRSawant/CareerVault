"""add authentication audit logs and sessions

Revision ID: e2f7a4c9d631
Revises: c8d4a2f1b907
Create Date: 2026-08-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e2f7a4c9d631"
down_revision: Union[str, None] = "c8d4a2f1b907"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column(
            "auth_method",
            sa.Enum(
                "LOGIN",
                "REGISTRATION",
                name="autheventtype",
                native_enum=False,
                length=20,
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "end_reason",
            sa.Enum(
                "LOGOUT",
                "ACCOUNT_BLOCKED",
                name="authsessionendreason",
                native_enum=False,
                length=30,
                create_constraint=True,
            ),
            nullable=True,
        ),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("user_agent", sa.String(length=512), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_auth_sessions_user_id", "auth_sessions", ["user_id"]
    )
    op.create_index(
        "ix_auth_sessions_started_at", "auth_sessions", ["started_at"]
    )
    op.create_index(
        "ix_auth_sessions_expires_at", "auth_sessions", ["expires_at"]
    )

    op.create_table(
        "login_audit_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("auth_session_id", sa.Uuid(), nullable=True),
        sa.Column(
            "event_type",
            sa.Enum(
                "LOGIN",
                "REGISTRATION",
                name="auditeventtype",
                native_enum=False,
                length=20,
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.Column(
            "outcome",
            sa.Enum(
                "SUCCESS",
                "FAILURE",
                name="authoutcome",
                native_enum=False,
                length=20,
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.Column(
            "failure_reason",
            sa.Enum(
                "INVALID_CREDENTIALS",
                "ACCOUNT_BLOCKED",
                "ROLE_NOT_ALLOWED",
                name="authfailurereason",
                native_enum=False,
                length=30,
                create_constraint=True,
            ),
            nullable=True,
        ),
        sa.Column(
            "role",
            sa.Enum(
                "JOB_APPLICANT",
                "SYSTEM_ADMIN",
                name="audituserrole",
                native_enum=False,
                length=30,
                create_constraint=True,
            ),
            nullable=True,
        ),
        sa.Column("identifier_hash", sa.String(length=64), nullable=False),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("user_agent", sa.String(length=512), nullable=True),
        sa.Column("http_status", sa.SmallInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["auth_session_id"],
            ["auth_sessions.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_login_audit_logs_user_id", "login_audit_logs", ["user_id"]
    )
    op.create_index(
        "ix_login_audit_logs_auth_session_id",
        "login_audit_logs",
        ["auth_session_id"],
    )
    op.create_index(
        "ix_login_audit_logs_event_type",
        "login_audit_logs",
        ["event_type"],
    )
    op.create_index(
        "ix_login_audit_logs_outcome", "login_audit_logs", ["outcome"]
    )
    op.create_index(
        "ix_login_audit_logs_role", "login_audit_logs", ["role"]
    )
    op.create_index(
        "ix_login_audit_logs_identifier_hash",
        "login_audit_logs",
        ["identifier_hash"],
    )
    op.create_index(
        "ix_login_audit_logs_occurred_at",
        "login_audit_logs",
        ["occurred_at"],
    )


def downgrade() -> None:
    op.drop_table("login_audit_logs")
    op.drop_table("auth_sessions")
