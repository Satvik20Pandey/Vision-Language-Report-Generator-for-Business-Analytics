from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from ..vectorstore import get_index
router = APIRouter(tags=["search"])
class SearchRequest(BaseModel):
	query: str
	limit: int = 5
@router.post("/search")
def search(payload: SearchRequest):
	index = get_index()
	results = index.search(payload.query, payload.limit)
	return {"results": [{"payload": p, "score": s} for p, s in results]}

