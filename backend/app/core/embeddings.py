from functools import lru_cache

from fastembed import TextEmbedding

from app.core.config import settings


class EmbeddingService:
	def __init__(self, model_name: str, dimension: int, batch_size: int) -> None:
		self.model_name = model_name
		self.dimension = dimension
		self.batch_size = batch_size
		self._model = TextEmbedding(model_name=model_name)

	def embed_text(self, text: str) -> list[float]:
		return self.embed_texts([text])[0]

	def embed_texts(self, texts: list[str]) -> list[list[float]]:
		vectors = self._model.embed(texts, batch_size=self.batch_size)
		return [vector.tolist() for vector in vectors]


@lru_cache()
def get_embedding_service() -> EmbeddingService:
	return EmbeddingService(
		model_name=settings.EMBEDDING_MODEL_NAME,
		dimension=settings.EMBEDDING_DIMENSION,
		batch_size=settings.EMBEDDING_BATCH_SIZE,
	)