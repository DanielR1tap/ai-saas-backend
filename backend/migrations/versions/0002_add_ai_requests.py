"""add ai requests

Revision ID: 0002_add_ai_requests
Revises: 0001_initial_schema
Create Date: 2026-06-01 00:00:01
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0002_add_ai_requests"
down_revision: str | None = "0001_initial_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ai_requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("system", sa.Text(), nullable=True),
        sa.Column("response_text", sa.Text(), nullable=False),
        sa.Column("provider", sa.String(length=80), nullable=False),
        sa.Column("ai_model", sa.String(length=120), nullable=False),
        sa.Column("credits", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_requests_id"), "ai_requests", ["id"], unique=False)
    op.create_index(op.f("ix_ai_requests_tenant_id"), "ai_requests", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_ai_requests_user_id"), "ai_requests", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_ai_requests_user_id"), table_name="ai_requests")
    op.drop_index(op.f("ix_ai_requests_tenant_id"), table_name="ai_requests")
    op.drop_index(op.f("ix_ai_requests_id"), table_name="ai_requests")
    op.drop_table("ai_requests")
