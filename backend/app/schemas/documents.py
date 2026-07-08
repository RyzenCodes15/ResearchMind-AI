from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentChunkResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True, extra="ignore")

	chunk_index: int
	page_start: int | None = None
	page_end: int | None = None
	content_length: int


class DocumentResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True, extra="ignore")

	id: int
	original_filename: str
	stored_filename: str
	storage_path: str
	file_hash: str
	file_size_bytes: int
	page_count: int | None = None
	chunk_count: int
	embedding_model: str | None = None
	chunk_size: int
	chunk_overlap: int
	status: str
	error_message: str | None = None
	created_at: datetime
	updated_at: datetime


class DocumentIngestionResponse(BaseModel):
	model_config = ConfigDict(extra="ignore")

	duplicate: bool = False
	document: DocumentResponse
	chunks: list[DocumentChunkResponse] = Field(default_factory=list)
	message: str