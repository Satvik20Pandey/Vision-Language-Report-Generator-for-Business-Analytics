from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import os
from ..database import get_db
from ..models import File as FileModel, FileType
from ..ai.text import analyze_csvs, synthesize_report, build_recommendations
from ..ai.vision import caption_images
from ..reporting import build_report_json, build_pdf
from ..config import settings
router = APIRouter(tags=["report"])
@router.post("/report")
def generate_report(payload: dict, db: Session = Depends(get_db)):
	ids: List[int] = payload.get("file_ids", [])
	want_pdf: bool = bool(payload.get("pdf", False))
	csv_paths = []
	img_paths = []
	for fid in ids:
		obj = db.query(FileModel).filter(FileModel.id == fid).first()
		if not obj:
			continue
		if obj.filetype == FileType.csv:
			csv_paths.append(obj.path)
		else:
			img_paths.append(obj.path)
	csv_metrics, trends, recs_seed = analyze_csvs(csv_paths)
	captions = caption_images(img_paths) if img_paths else []
	summary = synthesize_report(csv_metrics, trends, captions)
	recs = build_recommendations(trends, csv_metrics)
	recs = list(dict.fromkeys(recs_seed + recs))
	report = build_report_json(summary, csv_metrics, trends, recs, captions)
	pdf_file = None
	if want_pdf:
		os.makedirs("reports", exist_ok=True)
		out_path = os.path.join("reports", "report.pdf")
		build_pdf(out_path, report, settings.report_font)
		pdf_file = out_path
	return {"report": report.model_dump(), "pdf_file": pdf_file}

