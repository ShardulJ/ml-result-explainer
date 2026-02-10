from fastapi import APIRouter, HTTPException, Depends
from ..models.schemas import AnalysisResult
from ..services.ingestion import IngestionService
from ..core.config import settings

router = APIRouter(prefix="/analyze", tags=["Analysis"])

def get_ingestion_service():
    return IngestionService(upload_dir=settings.UPLOAD_DIR, report_dir=settings.REPORT_DIR)

@router.post("/{upload_id}", response_model=AnalysisResult)
async def analyze_upload(upload_id: str, service: IngestionService = Depends(get_ingestion_service)):
    result = await service.analyze_upload(upload_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Upload {upload_id} not found")
    return result