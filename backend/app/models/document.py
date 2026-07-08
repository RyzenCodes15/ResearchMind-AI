from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DocumentStatus(StrEnum):
	PENDING = "pending"
	PROCESSING = "processing"
	COMPLETED = "completed"
	FAILED = "failed"
	DUPLICATE = "duplicate"


class Document(Base):
	__tablename__ = "documents"
	__table_args__ = (UniqueConstraint("file_hash", name="uq_documents_file_hash"),)

	id: Mapped[int] = mapped_column(primary_key=True)
	original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
	stored_filename: Mapped[str] = mapped_column(String(255), nullable=False)
	storage_path: Mapped[str] = mapped_column(String(512), nullable=False)
	file_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
	file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
	page_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
	chunk_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
	embedding_model: Mapped[str | None] = mapped_column(String(255), nullable=True)
	chunk_size: Mapped[int] = mapped_column(Integer, nullable=False)
	chunk_overlap: Mapped[int] = mapped_column(Integer, nullable=False)
	status: Mapped[str] = mapped_column(String(32), nullable=False, default=DocumentStatus.PENDING)
	error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
		onupdate=func.now(),
	)

	chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")