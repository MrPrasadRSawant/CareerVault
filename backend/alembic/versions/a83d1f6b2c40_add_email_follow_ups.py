"""add recruiter email follow-ups

Revision ID: a83d1f6b2c40
Revises: f7a4c2d9e1b6
Create Date: 2026-08-13
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a83d1f6b2c40"
down_revision: Union[str, None] = "f7a4c2d9e1b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "email_follow_ups",
        sa.Column("application_id", sa.Uuid(), nullable=False),
        sa.Column("external_message_id", sa.String(length=500), nullable=True),
        sa.Column("thread_id", sa.String(length=500), nullable=True),
        sa.Column("subject", sa.String(length=500), nullable=False),
        sa.Column("sender_email", sa.String(length=320), nullable=False),
        sa.Column("sender_name", sa.String(length=255), nullable=True),
        sa.Column("recipient_emails", sa.JSON(), nullable=True),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("body_text", sa.Text(), nullable=True),
        sa.Column(
            "outcome",
            sa.Enum("PENDING", "WON", "LOST", name="emailfollowupoutcome", native_enum=False, length=30),
            nullable=False,
        ),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("reason_category", sa.String(length=100), nullable=True),
        sa.Column("ai_confidence", sa.Float(), nullable=True),
        sa.Column("raw_metadata", sa.JSON(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["application_id"], ["applications.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("application_id", "external_message_id", name="uq_email_follow_ups_application_message"),
    )
    op.create_index("ix_email_follow_ups_application_id", "email_follow_ups", ["application_id"])
    op.create_index("ix_email_follow_ups_external_message_id", "email_follow_ups", ["external_message_id"])
    op.create_index("ix_email_follow_ups_thread_id", "email_follow_ups", ["thread_id"])
    op.create_index("ix_email_follow_ups_sender_email", "email_follow_ups", ["sender_email"])
    op.create_index("ix_email_follow_ups_received_at", "email_follow_ups", ["received_at"])
    op.create_index("ix_email_follow_ups_outcome", "email_follow_ups", ["outcome"])
    op.create_index("ix_email_follow_ups_reason_category", "email_follow_ups", ["reason_category"])


def downgrade() -> None:
    op.drop_table("email_follow_ups")
