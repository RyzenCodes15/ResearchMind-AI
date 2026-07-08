from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.app_info import get_app_info_service
from app.schemas.health import DatabaseHealthResponse, HealthResponse
from app.services.app_info import AppInfoService

router = APIRouter()


@router.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check() -> HealthResponse:
	return HealthResponse(status="ok")


@router.get(
	"/health/db",
	response_model=DatabaseHealthResponse,
	summary="Database health check",
)
def database_health_check(
	db: Session = Depends(get_db),
	service: AppInfoService = Depends(get_app_info_service),
) -> DatabaseHealthResponse:
	db.execute(text("SELECT 1"))
	app_info = service.get_app_info()
	if app_info is None:
		raise HTTPException(
			status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
			detail="Database is reachable, but the application metadata row is missing.",
		)

	return DatabaseHealthResponse(status="ok", database="connected", app_info=app_info)