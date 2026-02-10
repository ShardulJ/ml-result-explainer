from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from ..models.schemas import UploadResponse, UploadDetail
from ..services.ingestion import IngestionService
from ..core.config import settings

router = APIRouter(prefix="/upload", tags=["Upload"])

def get_ingestion_service():
    return IngestionService(upload_dir=settings.UPLOAD_DIR, report_dir=settings.REPORT_DIR)

@router.post("", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...), service: IngestionService = Depends(get_ingestion_service)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files accepted")
    
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    result = await service.process_upload(file.filename, content)
    if result.status == "failed":
        raise HTTPException(status_code=400, detail=result.message)
    
    return result

@router.get("/{upload_id}", response_model=UploadDetail)
async def get_upload(upload_id: str, service: IngestionService = Depends(get_ingestion_service)):
    detail = await service.get_upload_detail(upload_id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Upload {upload_id} not found")
    return detail