from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings
from app.core.embeddings import EmbeddingService
from app.core.storage import DocumentStorage
from app.models.document import Document, DocumentStatus
from app.models.document_chunk import DocumentChunk
from app.repositories.document import DocumentRepository
from app.repositories.document_chunk import DocumentChunkRepository
from app.schemas.documents import (
	DocumentChunkResponse,
	DocumentIngestionResponse,
	DocumentResponse,
)
from app.utils.chunking import split_into_semantic_chunks
from app.utils.pdf import extract_pdf_text
from app.utils.text import normalize_text

ALLOWED_CONTENT_TYPES = {"application/pdf"}
MAX_UPLOAD_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


@dataclass(slots=True)
class PreparedUpload:
	file_hash: str
	file_size_bytes: int
	temp_path: Path
	original_filename: str


class DocumentIngestionService:
	def __init__(
		self,
		document_repository: DocumentRepository,
		chunk_repository: DocumentChunkRepository,
		storage: DocumentStorage,
		embedding_service: EmbeddingService,
	) -> None:
		self.document_repository = document_repository
		self.chunk_repository = chunk_repository
		self.storage = storage
		self.embedding_service = embedding_service

	async def ingest(self, upload_file: UploadFile) -> DocumentIngestionResponse:
		self._validate_upload(upload_file)
		prepared: PreparedUpload | None = None
		document: Document | None = None

		try:
			prepared = await self._prepare_upload(upload_file)
			existing = self.document_repository.get_by_hash(prepared.file_hash)
			if existing is not None:
				if existing.status == DocumentStatus.FAILED:
					self.document_repository.delete(existing)
				else:
					self._cleanup_path(prepared.temp_path)
					return DocumentIngestionResponse(
						duplicate=True,
						document=self._document_to_response(existing),
						chunks=[self._chunk_to_response(chunk) for chunk in existing.chunks],
						message="Duplicate PDF skipped",
					)

			final_path = self.storage.build_final_path(prepared.file_hash, prepared.original_filename)
			prepared.temp_path.replace(final_path)

			document = self._create_document_record(prepared, final_path)
			self.document_repository.session.commit()

			try:
				raw_text, page_count = extract_pdf_text(final_path)
				normalized_text = normalize_text(raw_text)
				if not normalized_text:
					raise ValueError("The uploaded PDF does not contain extractable text.")

				chunk_texts = split_into_semantic_chunks(
					normalized_text,
					chunk_size=settings.CHUNK_SIZE,
					overlap=settings.CHUNK_OVERLAP,
				)
				if not chunk_texts:
					raise ValueError("The uploaded PDF could not be split into chunks.")

				embeddings = self.embedding_service.embed_texts(chunk_texts)
				chunk_records = self._build_chunk_records(document.id, chunk_texts, embeddings)
				self.chunk_repository.create_many(chunk_records)
				document.page_count = page_count
				document.chunk_count = len(chunk_records)
				document.embedding_model = settings.EMBEDDING_MODEL_NAME
				document.status = DocumentStatus.COMPLETED
				document.error_message = None
				self.document_repository.session.commit()

				return DocumentIngestionResponse(
					duplicate=False,
					document=self._document_to_response(document),
					chunks=[self._chunk_to_response(chunk) for chunk in chunk_records],
					message="Document ingested successfully",
				)
			except Exception as exc:
				self.document_repository.session.rollback()
				if document is not None:
					document.status = DocumentStatus.FAILED
					document.error_message = str(exc)
					self.document_repository.session.add(document)
					self.document_repository.session.commit()
				raise HTTPException(
					status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
					detail=f"Document ingestion failed: {exc}",
				) from exc
		finally:
			await upload_file.close()
			if prepared is not None:
				self._cleanup_path(prepared.temp_path)

	async def list_documents(self) -> list[DocumentResponse]:
		documents = self.document_repository.list(limit=1000)
		return [self._document_to_response(doc) for doc in documents]

	async def delete_document(self, document_id: int) -> None:
		document = self.document_repository.get(document_id)
		if not document:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Document not found",
			)
		
		storage_path = Path(document.storage_path)
		if storage_path.exists():
			self._cleanup_path(storage_path)

		self.document_repository.delete(document)
		self.document_repository.session.commit()

	def _validate_upload(self, upload_file: UploadFile) -> None:
		if upload_file.content_type not in ALLOWED_CONTENT_TYPES:
			raise HTTPException(
				status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
				detail="Only PDF files are supported.",
			)

		if not (upload_file.filename or "").lower().endswith(".pdf"):
			raise HTTPException(
				status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
				detail="The uploaded file must have a .pdf extension.",
			)

	async def _prepare_upload(self, upload_file: UploadFile) -> PreparedUpload:
		temp_path = self.storage.build_temp_path(uuid4().hex)
		hasher = sha256()
		total_bytes = 0

		with temp_path.open("wb") as temp_file:
			while True:
				chunk = await upload_file.read(1024 * 1024)
				if not chunk:
					break
				total_bytes += len(chunk)
				if total_bytes > MAX_UPLOAD_BYTES:
					self._cleanup_path(temp_path)
					raise HTTPException(
						status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
						detail=f"PDF uploads are limited to {settings.MAX_UPLOAD_SIZE_MB} MB.",
					)
				hasher.update(chunk)
				temp_file.write(chunk)

		return PreparedUpload(
			file_hash=hasher.hexdigest(),
			file_size_bytes=total_bytes,
			temp_path=temp_path,
			original_filename=upload_file.filename or f"document-{uuid4().hex}.pdf",
		)

	def _create_document_record(self, prepared: PreparedUpload, final_path: Path) -> Document:
		document = Document(
			original_filename=prepared.original_filename,
			stored_filename=final_path.name,
			storage_path=str(final_path),
			file_hash=prepared.file_hash,
			file_size_bytes=prepared.file_size_bytes,
			chunk_count=0,
			chunk_size=settings.CHUNK_SIZE,
			chunk_overlap=settings.CHUNK_OVERLAP,
			status=DocumentStatus.PROCESSING,
		)
		self.document_repository.session.add(document)
		self.document_repository.session.flush()
		return document

	def _build_chunk_records(
		self,
		document_id: int,
		chunk_texts: list[str],
		embeddings: list[list[float]],
	) -> list[DocumentChunk]:
		chunk_records: list[DocumentChunk] = []
		for index, (chunk_text, embedding) in enumerate(zip(chunk_texts, embeddings, strict=True)):
			chunk_records.append(
				DocumentChunk(
					document_id=document_id,
					chunk_index=index,
					content=chunk_text,
					page_start=None,
					page_end=None,
					content_length=len(chunk_text),
					embedding=embedding,
				)
			)
		return chunk_records

	def _document_to_response(self, document: Document) -> DocumentResponse:
		return DocumentResponse.model_validate(document)

	def _chunk_to_response(self, chunk: DocumentChunk) -> DocumentChunkResponse:
		return DocumentChunkResponse.model_validate(chunk)

	def _cleanup_path(self, path: Path) -> None:
		if path.exists():
			path.unlink()