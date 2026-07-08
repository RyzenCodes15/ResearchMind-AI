"""documents ingestion

Revision ID: 0002_documents_ingestion
Revises: 0001_initial
Create Date: 2026-07-08 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


revision = "0002_documents_ingestion"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
	op.create_table(
		"documents",
		sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
		sa.Column("original_filename", sa.String(length=255), nullable=False),
		sa.Column("stored_filename", sa.String(length=255), nullable=False),
		sa.Column("storage_path", sa.String(length=512), nullable=False),
		sa.Column("file_hash", sa.String(length=64), nullable=False),
		sa.Column("file_size_bytes", sa.Integer(), nullable=False),
		sa.Column("page_count", sa.Integer(), nullable=True),
		sa.Column("chunk_count", sa.Integer(), nullable=False, server_default="0"),
		sa.Column("embedding_model", sa.String(length=255), nullable=True),
		sa.Column("chunk_size", sa.Integer(), nullable=False),
		sa.Column("chunk_overlap", sa.Integer(), nullable=False),
		sa.Column("status", sa.String(length=32), nullable=False),
		sa.Column("error_message", sa.Text(), nullable=True),
		sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
		sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
		sa.UniqueConstraint("file_hash", name="uq_documents_file_hash"),
	)
	op.create_index(op.f("ix_documents_file_hash"), "documents", ["file_hash"], unique=False)

	op.create_table(
		"document_chunks",
		sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
		sa.Column("document_id", sa.Integer(), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
		sa.Column("chunk_index", sa.Integer(), nullable=False),
		sa.Column("content", sa.Text(), nullable=False),
		sa.Column("page_start", sa.Integer(), nullable=True),
		sa.Column("page_end", sa.Integer(), nullable=True),
		sa.Column("content_length", sa.Integer(), nullable=False),
		sa.Column("embedding", Vector(384), nullable=False),
		sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
	)
	op.create_index(op.f("ix_document_chunks_document_id"), "document_chunks", ["document_id"], unique=False)


def downgrade() -> None:
	op.drop_index(op.f("ix_document_chunks_document_id"), table_name="document_chunks")
	op.drop_table("document_chunks")
	op.drop_index(op.f("ix_documents_file_hash"), table_name="documents")
	op.drop_table("documents")