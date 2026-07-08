from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.core.config import settings
from app.schemas.system import AppInfoResponse

router = APIRouter(tags=["root"])
router.include_router(health_router)


@router.get("/", response_model=AppInfoResponse, summary="Application info")
async def root() -> AppInfoResponse:
	return AppInfoResponse(
		name=settings.APP_NAME,
		version=settings.APP_VERSION,
		status="ok",
	)