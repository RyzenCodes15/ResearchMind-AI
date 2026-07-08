from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers

def create_app() -> FastAPI:
	app = FastAPI(
		title=settings.APP_NAME,
		description=settings.APP_DESCRIPTION,
		version=settings.APP_VERSION,
	)

	if settings.BACKEND_CORS_ORIGINS:
		app.add_middleware(
			CORSMiddleware,
			allow_origins=settings.BACKEND_CORS_ORIGINS,
			allow_credentials=True,
			allow_methods=["*"],
			allow_headers=["*"],
		)

	register_exception_handlers(app)
	app.include_router(api_router)
	return app


app = create_app()
