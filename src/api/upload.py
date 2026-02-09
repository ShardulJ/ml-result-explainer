from fastapi import APIRouter, UploadFile, File, HTTPException, Depaends
from ..models.schemas import UploadResponse, UploadDetail
from ..services.ingestion import Ingestion Service
from ..core.config import settings

router = APIRouter(prefix='/upload', tags =["Upload"])

def get_ingestion_service():
	pass

def upload_csv():
	pass

def get_upload():
	pass