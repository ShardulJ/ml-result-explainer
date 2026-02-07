from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
	APP_NAME : str = "ML Results Exp[lainer"
	VERSION : str = "1.0.0"
	DEBUG : bool = True
	API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["*"]
    DATABASE_URL: str = "sqlite+aiosqlite:///./ml_explainer.db"
    UPLOAD_DIR: str = "./data/uploads"
    REPORT_DIR: str = "./data/reports"
    MAX_UPLOAD_SIZE: int = 52_428_800
    ANTHROPIC_API_KEY: str = ""
    LLM_MODEL: str = "claude-sonnet-4-20250514"
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.3
    MAX_FEATURES_DISPLAY: int = 10
    ANOMALY_THRESHOLD: float = 3.0
	
	class Config:
		env_file = ".env"
		case_sensitive = True

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.REPORT_DIR, exist_ok=True)
