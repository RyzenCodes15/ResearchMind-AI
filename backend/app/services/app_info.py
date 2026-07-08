from app.models.app_info import AppInfo
from app.repositories.app_info import AppInfoRepository
from app.services.base import BaseService


class AppInfoService(BaseService[AppInfoRepository]):
	def get_app_info(self) -> AppInfo | None:
		return self.repository.get_app_info()