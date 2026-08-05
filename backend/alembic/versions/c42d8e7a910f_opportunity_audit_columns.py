"""replace opportunity metadata and timestamps with audit columns

Revision ID: c42d8e7a910f
Revises: b71f2a9c4d11
Create Date: 2026-08-06
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c42d8e7a910f"
down_revision: Union[str, None] = "b71f2a9c4d11"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("job_opportunities", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_by", sa.Uuid(), nullable=True))
        batch_op.add_column(sa.Column("created_on_utc", sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column("updated_by", sa.Uuid(), nullable=True))
        batch_op.add_column(sa.Column("updated_on_utc", sa.DateTime(timezone=True), nullable=True))
        batch_op.create_foreign_key("fk_job_opportunities_created_by_users", "users", ["created_by"], ["id"])
        batch_op.create_foreign_key("fk_job_opportunities_updated_by_users", "users", ["updated_by"], ["id"])

    op.execute(
        "UPDATE job_opportunities "
        "SET created_by = user_id, updated_by = user_id, "
        "created_on_utc = created_at, updated_on_utc = updated_at"
    )

    op.create_index("ix_job_opportunities_created_by", "job_opportunities", ["created_by"])
    op.create_index("ix_job_opportunities_updated_by", "job_opportunities", ["updated_by"])

    with op.batch_alter_table("job_opportunities", schema=None) as batch_op:
        batch_op.alter_column("created_by", existing_type=sa.Uuid(), nullable=False)
        batch_op.alter_column("created_on_utc", existing_type=sa.DateTime(timezone=True), nullable=False)
        batch_op.alter_column("updated_by", existing_type=sa.Uuid(), nullable=False)
        batch_op.alter_column("updated_on_utc", existing_type=sa.DateTime(timezone=True), nullable=False)
        batch_op.drop_column("extra_metadata")
        batch_op.drop_column("created_at")
        batch_op.drop_column("updated_at")


def downgrade() -> None:
    op.drop_index("ix_job_opportunities_updated_by", table_name="job_opportunities")
    op.drop_index("ix_job_opportunities_created_by", table_name="job_opportunities")

    with op.batch_alter_table("job_opportunities", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_at", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("extra_metadata", sa.JSON(), nullable=True))

    op.execute(
        "UPDATE job_opportunities "
        "SET created_at = created_on_utc, updated_at = updated_on_utc"
    )

    with op.batch_alter_table("job_opportunities", schema=None) as batch_op:
        batch_op.drop_constraint("fk_job_opportunities_created_by_users", type_="foreignkey")
        batch_op.drop_constraint("fk_job_opportunities_updated_by_users", type_="foreignkey")
        batch_op.drop_column("created_by")
        batch_op.drop_column("created_on_utc")
        batch_op.drop_column("updated_by")
        batch_op.drop_column("updated_on_utc")
