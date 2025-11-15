from fastapi import FastAPI
from .routers.ingest import router as ingest_router
from .routers.report import router as report_router
from .routers.search import router as search_router
app = FastAPI(title="Vision-Language Report Generator", version="1.0.0")
@app.get("/health")
def health():
	return {"status": "ok"}
app.include_router(ingest_router, prefix="/api")
app.include_router(report_router, prefix="/api")
app.include_router(search_router, prefix="/api")

