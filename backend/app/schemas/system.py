from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppInfoResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True, extra="ignore")

	name: str
	version: str
	status: str


class AppInfoRecordResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True, extra="ignore")

	id: int
	name: str
	version: str
	environment: str
	created_at: datetime
	updated_at: datetime