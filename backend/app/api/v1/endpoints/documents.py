from fastapi import APIRouter, Depends, File, UploadFile, status

from app.dependencies.documents import get_document_ingestion_service
from app.schemas.documents import DocumentIngestionResponse
from app.services.documents import DocumentIngestionService

router = APIRouter(prefix="/documents")


@router.post(
	"/upload",
	response_model=DocumentIngestionResponse,
	status_code=status.HTTP_201_CREATED,
	summary="Upload and ingest a PDF document",
)
async def upload_document(
	file: UploadFile = File(...),
	service: DocumentIngestionService = Depends(get_document_ingestion_service),
) -> DocumentIngestionResponse:
	return await service.ingest(file)