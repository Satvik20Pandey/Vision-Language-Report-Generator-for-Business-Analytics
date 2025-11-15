from pydantic import BaseModel
from typing import List, Optional, Any
class IngestResponseItem(BaseModel):
	id: int
	filename: str
	filetype: str
class IngestResponse(BaseModel):
	items: List[IngestResponseItem]
class ReportRequest(BaseModel):
	file_ids: List[int]
	pdf: bool = False
class KeyMetric(BaseModel):
	name: str
	value: Any
class ReportSection(BaseModel):
	title: str
	content: str
class ReportJSON(BaseModel):
	summary: str
	key_metrics: List[KeyMetric]
	trends: List[str]
	recommendations: List[str]
	visual_insights: List[str]
class ReportResponse(BaseModel):
	report: ReportJSON
	pdf_file: Optional[str] = None

