from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    return {
        "message": "ResearchMind AI API v1",
        "status": "healthy",
    }
