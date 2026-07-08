from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
	def __init__(self, session: Session, model: type[ModelType]) -> None:
		self.session = session
		self.model = model

	def get(self, object_id: Any) -> ModelType | None:
		return self.session.get(self.model, object_id)

	def list(self, offset: int = 0, limit: int = 100) -> Sequence[ModelType]:
		statement = select(self.model).offset(offset).limit(limit)
		return self.session.scalars(statement).all()

	def create(self, data: dict[str, Any]) -> ModelType:
		obj = self.model(**data)
		self.session.add(obj)
		self.session.flush()
		self.session.refresh(obj)
		return obj

	def delete(self, obj: ModelType) -> None:
		self.session.delete(obj)
		self.session.flush()