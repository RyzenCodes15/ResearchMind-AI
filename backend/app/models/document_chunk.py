from __future__ import annotations

from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings
from app.db.base import Base


class DocumentChunk(Base):
	__tablename__ = "document_chunks"

	id: Mapped[int] = mapped_column(primary_key=True)
	document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), index=True, nullable=False)
	chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
	content: Mapped[str] = mapped_column(Text, nullable=False)
	page_start: Mapped[int | None] = mapped_column(Integer, nullable=True)
	page_end: Mapped[int | None] = mapped_column(Integer, nullable=True)
	content_length: Mapped[int] = mapped_column(Integer, nullable=False)
	embedding: Mapped[list[float]] = mapped_column(Vector(settings.EMBEDDING_DIMENSION), nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

	document = relationship("Document", back_populates="chunks")