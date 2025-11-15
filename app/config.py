import os
from pydantic import BaseModel
class Settings(BaseModel):
	app_name: str = "Vision-Language Report Generator"
	database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
	aws_access_key_id: str | None = os.getenv("AWS_ACCESS_KEY_ID")
	aws_secret_access_key: str | None = os.getenv("AWS_SECRET_ACCESS_KEY")
	aws_region: str | None = os.getenv("AWS_REGION")
	s3_bucket: str | None = os.getenv("S3_BUCKET")
	storage_dir: str = os.getenv("STORAGE_DIR", "storage")
	qdrant_url: str | None = os.getenv("QDRANT_URL")
	qdrant_api_key: str | None = os.getenv("QDRANT_API_KEY")
	openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
	report_font: str | None = os.getenv("REPORT_FONT")
class Config:
	arbitrary_types_allowed = True
settings = Settings()

