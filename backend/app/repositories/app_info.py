from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.app_info import AppInfo
from app.repositories.base import BaseRepository


class AppInfoRepository(BaseRepository[AppInfo]):
	def __init__(self, session: Session) -> None:
		super().__init__(session=session, model=AppInfo)

	def get_app_info(self) -> AppInfo | None:
		statement = select(AppInfo).order_by(AppInfo.id.asc()).limit(1)
		return self.session.scalar(statement)