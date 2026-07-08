from functools import lru_cache

from google import genai

from app.core.config import settings


class GeminiService:
	def __init__(self, api_key: str | None, model_name: str) -> None:
		self.api_key = api_key
		self.model_name = model_name
		self._client: genai.Client | None = None

	def _get_client(self) -> genai.Client:
		if self._client is not None:
			return self._client

		if not self.api_key:
			raise RuntimeError("GEMINI_API_KEY is not configured")

		self._client = genai.Client(api_key=self.api_key)
		return self._client

	def generate_content(self, **kwargs):
		client = self._get_client()
		return client.models.generate_content(model=self.model_name, **kwargs)


@lru_cache()
def get_gemini_service() -> GeminiService:
	return GeminiService(
		api_key=settings.GEMINI_API_KEY,
		model_name=settings.GEMINI_MODEL_NAME,
	)