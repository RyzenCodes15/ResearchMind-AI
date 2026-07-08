from fastapi import APIRouter, Depends, status

from app.dependencies.chat import get_chat_service
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import ChatService

router = APIRouter(prefix="/chat")


@router.post(
	"",
	response_model=ChatResponse,
	status_code=status.HTTP_200_OK,
	summary="Answer a question using uploaded documents",
)
async def chat(
	payload: ChatRequest,
	service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
	return await service.chat(payload)