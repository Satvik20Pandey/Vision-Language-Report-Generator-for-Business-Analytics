import os
import sys
import unittest
from fastapi.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app
class HealthTest(unittest.TestCase):
	def test_health(self):
		client = TestClient(app)
		r = client.get("/health")
		assert r.status_code == 200
		assert r.json().get("status") == "ok"
if __name__ == "__main__":
	unittest.main()

