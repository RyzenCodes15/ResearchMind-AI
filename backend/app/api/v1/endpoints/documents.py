from fastapi import APIRouter, Depends, File, UploadFile, status

from app.dependencies.documents import get_document_ingestion_service
from app.schemas.documents import DocumentIngestionResponse, DocumentResponse
from app.services.documents import DocumentIngestionService

router = APIRouter(prefix="/documents")


@router.get(
	"",
	response_model=list[DocumentResponse],
	status_code=status.HTTP_200_OK,
	summary="List all uploaded documents",
)
async def list_documents(
	service: DocumentIngestionService = Depends(get_document_ingestion_service),
) -> list[DocumentResponse]:
	return await service.list_documents()


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


@router.delete(
	"/{document_id}",
	status_code=status.HTTP_204_NO_CONTENT,
	summary="Delete a document",
)
async def delete_document(
	document_id: int,
	service: DocumentIngestionService = Depends(get_document_ingestion_service),
) -> None:
	await service.delete_document(document_id)