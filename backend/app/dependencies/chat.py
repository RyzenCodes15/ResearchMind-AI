from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.embeddings import EmbeddingService, get_embedding_service
from app.core.gemini import GeminiService, get_gemini_service
from app.dependencies.db import get_db
from app.repositories.document_chunk import DocumentChunkRepository
from app.services.chat import ChatService


def get_document_chunk_repository(db: Session = Depends(get_db)) -> DocumentChunkRepository:
	return DocumentChunkRepository(db)


def get_embedding_service_dependency() -> EmbeddingService:
	return get_embedding_service()


def get_gemini_service_dependency() -> GeminiService:
	return get_gemini_service()


def get_chat_service(
	document_chunk_repository: DocumentChunkRepository = Depends(get_document_chunk_repository),
	embedding_service: EmbeddingService = Depends(get_embedding_service_dependency),
	gemini_service: GeminiService = Depends(get_gemini_service_dependency),
) -> ChatService:
	return ChatService(
		document_chunk_repository=document_chunk_repository,
		embedding_service=embedding_service,
		gemini_service=gemini_service,
	)