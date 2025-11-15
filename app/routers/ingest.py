from fastapi import APIRouter, UploadFile, File, Depends
from typing import List
import os
from sqlalchemy.orm import Session
from ..database import get_db, Base, engine
from ..models import File as FileModel, FileType
from ..storage import Storage
from ..vectorstore import get_index
Base.metadata.create_all(bind=engine)
router = APIRouter(tags=["ingest"])
@router.post("/ingest")
async def ingest(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
	storage = Storage()
	items = []
	index = get_index()
	for f in files:
		content = await f.read()
		path = storage.save(f.filename, content)
		filetype = FileType.csv if f.filename.lower().endswith(".csv") else FileType.image
		obj = FileModel(filename=f.filename, filetype=filetype, path=path, size=len(content), meta=None)
		db.add(obj)
		db.commit()
		db.refresh(obj)
		items.append({"id": obj.id, "filename": obj.filename, "filetype": obj.filetype.value})
		text = f"{obj.filename} {obj.filetype.value}"
		index.upsert([str(obj.id)], [text], [{"id": obj.id, "filename": obj.filename, "filetype": obj.filetype.value}])
	return {"items": items}

