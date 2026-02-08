import pandas as pd 
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
import os

from ..utils.validation import CSVValidator
from .profiling import DataProfiler
from .explainability import FeatureImportanceCalculator
from ..models.schemas import (
    UploadStatus, UploadResponse, UploadDetail,
    DataProfile, FeatureImportance, AnalysisResult
)

class IngestionService:

	def __init__(self, upload_dir: str, report_dir: str):
		self.upload_dir = upload_dir
        self.report_dir = report_dir
        self.validator = CSVValidator()
        self.profiler = DataProfiler()
        self.importance_calculator = FeatureImportanceCalculator()
        self.uploads = {}
        self.analyses = {}

	def process_upload(self, filename: str, file_content: bytes) -> UploadResponse:
		upload_id = str(uuid.uuid4())
        filepath = os.path.join(self.upload_dir, f"{upload_id}_{filename}")
        
        with open(filepath, 'wb') as f:
            f.write(file_content)

        is_valid, error_msg = self.validator.validate_file(filepath)
        if not is_valid:
            os.remove(filepath)
            return UploadResponse(
                upload_id=upload_id,
                filename=filename,
                status=UploadStatus.FAILED,
                upload_timestamp=datetime.now(),
                message=f"Validation failed: {error_msg}"
            )

        try:
        	df, metadata = self.validator.load_and_analyze(filepath)
            
            self.uploads[upload_id] = {
                "upload_id": upload_id,
                "filename": filename,
                "filepath": filepath,
                "status": UploadStatus.COMPLETE,
                "upload_timestamp": datetime.now(),
                **metadata
            }
            
            return UploadResponse(
                upload_id=upload_id,
                filename=filename,
                status=UploadStatus.COMPLETE,
                row_count=metadata["row_count"],
                column_count=metadata["column_count"],
                upload_timestamp=datetime.now(),
                message="Upload successful. Ready for analysis."
            )
        except Exception as e:
        	os.remove(filepath)
            return UploadResponse(
                upload_id=upload_id,
                filename=filename,
                status=UploadStatus.FAILED,
                upload_timestamp=datetime.now(),
                message=f"Processing failed: {str(e)}"
            )

	async def get_upload_detail(self, upload_id: str) -> Optional[UploadDetail]:
        if upload_id not in self.uploads:
            return None
        return UploadDetail(**self.uploads[upload_id])

	async def analyze_upload(self, upload_id: str) -> Optional[AnalysisResult]:
        if upload_id not in self.uploads:
            return None
        
        upload_data = self.uploads[upload_id]
        filepath = upload_data["filepath"]
        
        df = pd.read_csv(filepath)
        prediction_column = upload_data.get("prediction_column")
        
        profile_data = self.profiler.profile_data(df, prediction_column)
        anomalies = self.profiler.detect_anomalies(df, prediction_column)
        importance_scores = self.importance_calculator.calculate_importance(df, prediction_column)
        insights = self.importance_calculator.generate_insights(importance_scores)
        
        profile = DataProfile(**profile_data)
        feature_importances = [FeatureImportance(**imp) for imp in importance_scores]
        
        explanation = self._generate_explanation(profile_data, importance_scores, anomalies, insights)
        
        analysis_id = str(uuid.uuid4())
        result = AnalysisResult(
            analysis_id=analysis_id,
            upload_id=upload_id,
            status="complete",
            analysis_timestamp=datetime.now(),
            profile=profile,
            feature_importance=feature_importances,
            anomalies_detected=anomalies["total_anomalies"],
            anomaly_indices=anomalies["anomaly_indices"],
            explanation=explanation,
            insights=insights,
            confidence_score=0.85
        )
        
        self.analyses[analysis_id] = result
        return result

	def _generate_explaination(self, profile: Dict, importance: List[Dict], anomalies: Dict, insights: List[str]) -> str:
		pass

