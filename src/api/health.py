from fastapi import APIRouter
from datetime import datetime
from ..models.schemas import HealthResponse
from ..core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", version=settings.VERSION, timestamp=datetime.now())