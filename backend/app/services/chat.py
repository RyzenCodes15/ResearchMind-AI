from datetime import datetime, timezone
from textwrap import shorten

from fastapi import HTTPException, status
from google.genai import types
from pydantic import ValidationError
from starlette.concurrency import run_in_threadpool

from app.core.config import settings
from app.core.embeddings import EmbeddingService
from app.core.gemini import GeminiService
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.repositories.document_chunk import DocumentChunkRepository
from app.schemas.chat import ChatCitation, ChatRequest, ChatResponse, GeminiGroundedAnswer


class ChatService:
	def __init__(
		self,
		document_chunk_repository: DocumentChunkRepository,
		embedding_service: EmbeddingService,
		gemini_service: GeminiService,
	) -> None:
		self.document_chunk_repository = document_chunk_repository
		self.embedding_service = embedding_service
		self.gemini_service = gemini_service

	def _build_context(self, chunks: list[tuple[DocumentChunk, Document, float]]) -> str:
		lines: list[str] = []
		for index, (chunk, document, distance) in enumerate(chunks, start=1):
			page_label = "unknown"
			if chunk.page_start is not None and chunk.page_end is not None:
				page_label = str(chunk.page_start) if chunk.page_start == chunk.page_end else f"{chunk.page_start}-{chunk.page_end}"
			elif chunk.page_start is not None:
				page_label = str(chunk.page_start)

			lines.append(
				"\n".join(
					[
						f"Source {index}",
						f"Document: {document.original_filename}",
						f"Pages: {page_label}",
						f"Chunk index: {chunk.chunk_index}",
						f"Similarity distance: {distance:.4f}",
						f"Content: {chunk.content}",
					]
				)
			)
		return "\n\n".join(lines)

	def _build_prompt(self, question: str, context: str) -> str:
         return (
        "You are an AI research assistant.\n\n"
        "Answer the user's question ONLY using the information provided in the context below.\n\n"
        "If the answer is clearly present or can be reasonably summarized from the context, answer it directly.\n\n"
        "Only respond that the answer cannot be determined if the context genuinely does not contain enough information.\n\n"
        "Do not use outside knowledge.\n"
        "When possible, summarize naturally and clearly.\n\n"
        f"Question:\n{question}\n\n"
        f"Context:\n{context}"
    )

	def _parse_grounded_answer(self, response: object) -> GeminiGroundedAnswer:
		parsed = getattr(response, "parsed", None)
		if isinstance(parsed, GeminiGroundedAnswer):
			return parsed

		text = getattr(response, "text", None)
		if not text:
			raise ValueError("Gemini returned an empty response")

		try:
			return GeminiGroundedAnswer.model_validate_json(text)
		except ValidationError as exc:
			raise ValueError("Gemini response did not match the expected schema") from exc

	async def chat(self, request: ChatRequest) -> ChatResponse:
		question = request.question.strip()
		top_k = request.top_k or settings.CHAT_TOP_K
		question_embedding = self.embedding_service.embed_text(question)
		matches = self.document_chunk_repository.search_similar_chunks(question_embedding, top_k)
		best_similarity = max((max(0.0, 1.0 - distance) for _, _, distance in matches), default=0.0)

		if not matches or best_similarity < settings.CHAT_MIN_SIMILARITY:
			return ChatResponse(
				question=question,
				answer="I cannot determine the answer from the uploaded documents.",
				insufficient_context=True,
				model_name=self.gemini_service.model_name,
				retrieved_chunks=[],
				created_at=datetime.now(timezone.utc),
			)

		context = self._build_context(matches)
		prompt = self._build_prompt(question, context)
		try:
			response = await run_in_threadpool(
				self.gemini_service.generate_content,
				contents=prompt,
				config=types.GenerateContentConfig(
					temperature=0.0,
					max_output_tokens=512,
					response_mime_type="application/json",
					response_schema=GeminiGroundedAnswer,
					system_instruction=(
						"You answer research questions from uploaded documents only. "
						"If the uploaded context is insufficient, explicitly mark insufficient_context true."
					),
				),
			)
		except RuntimeError as exc:
			raise HTTPException(
				status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
				detail=str(exc),
			) from exc

		try:
			grounded_answer = self._parse_grounded_answer(response)
		except ValueError:
			grounded_answer = GeminiGroundedAnswer(
				answer="I cannot determine the answer from the uploaded documents.",
				insufficient_context=True,
			)

		retrieved_chunks = [
			ChatCitation(
				chunk_id=chunk.id,
				document_id=document.id,
				document_name=document.original_filename,
				chunk_index=chunk.chunk_index,
				page_start=chunk.page_start,
				page_end=chunk.page_end,
				similarity_score=max(0.0, 1.0 - distance),
				content=shorten(chunk.content, width=1000, placeholder="..."),
			)
			for chunk, document, distance in matches
		]

		if grounded_answer.insufficient_context:
			answer = "I cannot determine the answer from the uploaded documents."
		else:
			answer = grounded_answer.answer.strip()

		return ChatResponse(
			question=question,
			answer=answer,
			insufficient_context=grounded_answer.insufficient_context,
			model_name=self.gemini_service.model_name,
			retrieved_chunks=retrieved_chunks,
			created_at=datetime.now(timezone.utc),
		)