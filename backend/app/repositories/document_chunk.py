from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.repositories.base import BaseRepository


class DocumentChunkRepository(BaseRepository[DocumentChunk]):
	def __init__(self, session: Session) -> None:
		super().__init__(session=session, model=DocumentChunk)

	def create_many(self, chunks: Sequence[DocumentChunk]) -> None:
		self.session.add_all(list(chunks))

	def search_similar_chunks(
		self,
		query_embedding: list[float],
		top_k: int,
	) -> list[tuple[DocumentChunk, Document, float]]:
		distance = DocumentChunk.embedding.cosine_distance(query_embedding).label("distance")
		statement: Select[tuple[DocumentChunk, Document, float]] = (
			select(DocumentChunk, Document, distance)
			.join(Document, Document.id == DocumentChunk.document_id)
			.order_by(distance)
			.limit(top_k)
		)
		rows = self.session.execute(statement).all()
		return [(chunk, document, float(distance_value)) for chunk, document, distance_value in rows]