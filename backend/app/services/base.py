from typing import Generic, TypeVar

from app.repositories.base import BaseRepository

RepositoryType = TypeVar("RepositoryType")


class BaseService(Generic[RepositoryType]):
	def __init__(self, repository: RepositoryType) -> None:
		self.repository = repository