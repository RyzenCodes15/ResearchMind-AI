"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-07-08 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
	op.create_table(
		"app_info",
		sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
		sa.Column("name", sa.String(length=100), nullable=False),
		sa.Column("version", sa.String(length=32), nullable=False),
		sa.Column("environment", sa.String(length=32), nullable=False),
		sa.Column(
			"created_at",
			sa.DateTime(timezone=True),
			nullable=False,
			server_default=sa.text("now()"),
		),
		sa.Column(
			"updated_at",
			sa.DateTime(timezone=True),
			nullable=False,
			server_default=sa.text("now()"),
		),
	)
	op.create_index(op.f("ix_app_info_id"), "app_info", ["id"], unique=False)

	op.bulk_insert(
		sa.table(
			"app_info",
			sa.column("id", sa.Integer()),
			sa.column("name", sa.String()),
			sa.column("version", sa.String()),
			sa.column("environment", sa.String()),
		),
		[
			{
				"id": 1,
				"name": "ResearchMind AI",
				"version": "0.1.0",
				"environment": "development",
			},
		],
	)


def downgrade() -> None:
	op.drop_index(op.f("ix_app_info_id"), table_name="app_info")
	op.drop_table("app_info")