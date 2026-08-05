"""trim opportunities to the candidate-owned schema and remove companies

Revision ID: d5e91f7a2b30
Revises: c42d8e7a910f
Create Date: 2026-08-06
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d5e91f7a2b30"
down_revision: Union[str, None] = "c42d8e7a910f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("ix_job_opportunities_company_id", table_name="job_opportunities")
    op.drop_index("ix_job_opportunities_user_id", table_name="job_opportunities")

    with op.batch_alter_table("job_opportunities", schema=None) as batch_op:
        batch_op.drop_constraint("fk_job_opportunities_company_id_companies", type_="foreignkey")
        batch_op.drop_constraint("fk_job_opportunities_user_id_users", type_="foreignkey")
        for column in (
            "company_id",
            "user_id",
            "application_link",
            "salary_range",
            "source",
            "posted_date",
            "deadline",
            "notes",
        ):
            batch_op.drop_column(column)

    op.drop_table("companies")


def downgrade() -> None:
    raise NotImplementedError("The companies table and removed opportunity fields are intentionally not restored")
