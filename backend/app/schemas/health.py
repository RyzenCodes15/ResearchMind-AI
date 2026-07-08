from pydantic import BaseModel, ConfigDict

from app.schemas.system import AppInfoRecordResponse


class HealthResponse(BaseModel):
	model_config = ConfigDict(extra="ignore")

	status: str


class DatabaseHealthResponse(BaseModel):
	model_config = ConfigDict(extra="ignore")

	status: str
	database: str
	app_info: AppInfoRecordResponse