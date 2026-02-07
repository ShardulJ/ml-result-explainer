from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum

class UploadStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"

class UploadResponse(BaseModel):
    upload_id: str
    filename: str
    status: UploadStatus
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    upload_timestamp: datetime
    message: str = "Upload successful"

class UploadDetail(BaseModel):
    upload_id: str
    filename: str
    status: UploadStatus
    row_count: int
    column_count: int
    has_ground_truth: bool
    has_timestamp: bool
    column_names: List[str]
    prediction_column: Optional[str]
    upload_timestamp: datetime

class FeatureImportance(BaseModel):
    feature: str
    importance: float
    rank: int

class DataProfile(BaseModel):
    total_rows: int
    total_columns: int
    missing_values: Dict[str, int]
    missing_percentages: Dict[str, float]
    numeric_columns: List[str]
    categorical_columns: List[str]
    prediction_summary: Dict[str, Any]

class AnalysisResult(BaseModel):
    analysis_id: str
    upload_id: str
    status: str
    analysis_timestamp: datetime
    profile: DataProfile
    feature_importance: List[FeatureImportance]
    anomalies_detected: int
    anomaly_indices: List[int]
    explanation: Optional[str] = None
    insights: List[str] = []
    confidence_score: Optional[float] = None

class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str
    timestamp: datetime