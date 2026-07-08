from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):
	def __init__(self, session: Session) -> None:
		super().__init__(session=session, model=Document)

	def get_by_hash(self, file_hash: str) -> Document | None:
		statement = select(Document).where(Document.file_hash == file_hash)
		return self.session.scalar(statement)