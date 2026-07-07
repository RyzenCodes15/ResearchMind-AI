from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

app.include_router(
    api_router,
    prefix="/api/v1",
    tags=["v1"],
)