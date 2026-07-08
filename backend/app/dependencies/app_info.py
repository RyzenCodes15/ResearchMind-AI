from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.repositories.app_info import AppInfoRepository
from app.services.app_info import AppInfoService


def get_app_info_repository(db: Session = Depends(get_db)) -> AppInfoRepository:
	return AppInfoRepository(db)


def get_app_info_service(
	repository: AppInfoRepository = Depends(get_app_info_repository),
) -> AppInfoService:
	return AppInfoService(repository)