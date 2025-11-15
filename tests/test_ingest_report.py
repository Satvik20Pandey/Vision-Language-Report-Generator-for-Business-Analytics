import os
import sys
import io
import json
import unittest
from fastapi.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app
class IngestReportTest(unittest.TestCase):
	def test_ingest_and_report(self):
		os.environ["SKIP_VISION"] = "1"
		client = TestClient(app)
		csv_bytes = b"a,b,c\n1,2,3\n2,3,4\n3,4,5\n"
		img_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\nIDATx\x9cc`\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"
		files = [
			('files', ('data.csv', io.BytesIO(csv_bytes), 'text/csv')),
			('files', ('dot.png', io.BytesIO(img_bytes), 'image/png')),
		]
		r = client.post("/api/ingest", files=files)
		assert r.status_code == 200
		items = r.json()["items"]
		assert len(items) == 2
		ids = [it["id"] for it in items]
		r2 = client.post("/api/report", json={"file_ids": ids, "pdf": True})
		assert r2.status_code == 200
		body = r2.json()
		assert "report" in body
		assert "summary" in body["report"]
		assert body["report"]["key_metrics"]
		if body.get("pdf_file"):
			assert os.path.exists(body["pdf_file"])
if __name__ == "__main__":
	unittest.main()

