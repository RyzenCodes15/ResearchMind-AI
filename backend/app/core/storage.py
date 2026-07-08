from pathlib import Path

from app.core.config import settings


class DocumentStorage:
	def __init__(self, root_path: str) -> None:
		self.root_path = Path(root_path)
		self.uploads_path = self.root_path / "uploads"
		self.temp_path = self.root_path / "tmp"

	def ensure_directories(self) -> None:
		self.uploads_path.mkdir(parents=True, exist_ok=True)
		self.temp_path.mkdir(parents=True, exist_ok=True)

	def build_final_path(self, file_hash: str, original_filename: str) -> Path:
		suffix = Path(original_filename).suffix.lower() or ".pdf"
		return self.uploads_path / f"{file_hash}{suffix}"

	def build_temp_path(self, file_hash: str) -> Path:
		return self.temp_path / f"{file_hash}.upload"


def get_document_storage() -> DocumentStorage:
	storage = DocumentStorage(settings.DOCUMENT_STORAGE_PATH)
	storage.ensure_directories()
	return storage