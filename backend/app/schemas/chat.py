from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
	model_config = ConfigDict(extra="ignore")

	question: str = Field(min_length=1)
	top_k: int | None = Field(default=None, ge=1, le=20)
	document_ids: list[int] | None = Field(default=None, description="List of document IDs to restrict the search to.")


class ChatCitation(BaseModel):
	model_config = ConfigDict(from_attributes=True, extra="ignore")

	chunk_id: int
	document_id: int
	document_name: str
	chunk_index: int
	page_start: int | None
	page_end: int | None
	similarity_score: float
	content: str


class ChatResponse(BaseModel):
	model_config = ConfigDict(extra="ignore")

	question: str
	answer: str
	insufficient_context: bool
	model_name: str
	retrieved_chunks: list[ChatCitation] = Field(default_factory=list)
	created_at: datetime


class GeminiGroundedAnswer(BaseModel):
	model_config = ConfigDict(extra="ignore")

	answer: str = Field(description="The answer to the user's question based strictly on the provided context. If the answer cannot be determined from the context, provide a brief explanation.")
	insufficient_context: bool = Field(description="Set to true ONLY if the provided context does NOT contain enough information to answer the question. Set to false if the context DOES contain the answer.")