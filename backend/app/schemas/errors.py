from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
	model_config = ConfigDict(extra="ignore")

	detail: str


class ValidationErrorResponse(BaseModel):
	model_config = ConfigDict(extra="ignore")

	detail: str
	errors: list[dict[str, Any]] = Field(default_factory=list)