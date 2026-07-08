from collections.abc import Iterable

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.errors import ErrorResponse, ValidationErrorResponse


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
	return JSONResponse(
		status_code=exc.status_code,
		content=ErrorResponse(detail=str(exc.detail)).model_dump(),
	)


def validation_exception_handler(
	request: Request, exc: RequestValidationError
) -> JSONResponse:
	return JSONResponse(
		status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
		content=ValidationErrorResponse(
			detail="Request validation failed",
			errors=exc.errors(),
		).model_dump(mode="json"),
	)


def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
	return JSONResponse(
		status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
		content=ErrorResponse(detail="Internal server error").model_dump(),
	)


def register_exception_handlers(app: FastAPI) -> None:
	app.add_exception_handler(HTTPException, http_exception_handler)
	app.add_exception_handler(RequestValidationError, validation_exception_handler)
	app.add_exception_handler(Exception, unhandled_exception_handler)