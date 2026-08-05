"""add candidate opportunity fields and soft delete

Revision ID: b71f2a9c4d11
Revises: 97a0c76500ed
Create Date: 2026-08-06
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b71f2a9c4d11"
down_revision: Union[str, None] = "97a0c76500ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("job_opportunities", sa.Column("company_name", sa.String(255)))
    op.add_column("job_opportunities", sa.Column("post_url", sa.String(500)))
    op.add_column("job_opportunities", sa.Column("company_career_page", sa.String(500)))
    op.add_column("job_opportunities", sa.Column("company_url", sa.String(500)))
    op.add_column("job_opportunities", sa.Column("posted_on_utc", sa.DateTime(timezone=True)))
    op.add_column("job_opportunities", sa.Column("job_location", sa.String(255)))
    op.add_column("job_opportunities", sa.Column("extra_metadata", sa.JSON()))
    op.add_column(
        "job_opportunities",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_index(
        op.f("ix_job_opportunities_company_name"),
        "job_opportunities",
        ["company_name"],
    )
    op.create_index(
        op.f("ix_job_opportunities_is_deleted"),
        "job_opportunities",
        ["is_deleted"],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_job_opportunities_is_deleted"), table_name="job_opportunities")
    op.drop_index(op.f("ix_job_opportunities_company_name"), table_name="job_opportunities")
    op.drop_column("job_opportunities", "is_deleted")
    op.drop_column("job_opportunities", "extra_metadata")
    op.drop_column("job_opportunities", "job_location")
    op.drop_column("job_opportunities", "posted_on_utc")
    op.drop_column("job_opportunities", "company_url")
    op.drop_column("job_opportunities", "company_career_page")
    op.drop_column("job_opportunities", "post_url")
    op.drop_column("job_opportunities", "company_name")
