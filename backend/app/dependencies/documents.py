from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.embeddings import EmbeddingService, get_embedding_service
from app.core.storage import DocumentStorage, get_document_storage
from app.dependencies.db import get_db
from app.repositories.document import DocumentRepository
from app.repositories.document_chunk import DocumentChunkRepository
from app.services.documents import DocumentIngestionService


def get_document_repository(db: Session = Depends(get_db)) -> DocumentRepository:
	return DocumentRepository(db)


def get_document_chunk_repository(db: Session = Depends(get_db)) -> DocumentChunkRepository:
	return DocumentChunkRepository(db)


def get_document_storage_dependency() -> DocumentStorage:
	return get_document_storage()


def get_embedding_service_dependency() -> EmbeddingService:
	return get_embedding_service()


def get_document_ingestion_service(
	document_repository: DocumentRepository = Depends(get_document_repository),
	chunk_repository: DocumentChunkRepository = Depends(get_document_chunk_repository),
	storage: DocumentStorage = Depends(get_document_storage_dependency),
	embedding_service: EmbeddingService = Depends(get_embedding_service_dependency),
) -> DocumentIngestionService:
	return DocumentIngestionService(
		document_repository=document_repository,
		chunk_repository=chunk_repository,
		storage=storage,
		embedding_service=embedding_service,
	)