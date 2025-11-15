from typing import List, Tuple
from .config import settings
class VectorIndex:
	def __init__(self, collection: str = "files"):
		self.collection = collection
		self.client = None
		if settings.qdrant_url and settings.qdrant_api_key:
			try:
				from qdrant_client import QdrantClient  # type: ignore
				from qdrant_client.http import models as qmodels  # type: ignore
				self.client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
				try:
					self.client.get_collection(self.collection)
				except:
					self.client.recreate_collection(collection_name=self.collection, vectors_config=qmodels.VectorParams(size=384, distance=qmodels.Distance.COSINE))
			except:
				self.client = None
		self.memory_vectors: List[Tuple[str, list[float]]] = []
		self.memory_payloads: List[Tuple[str, dict]] = []
	def embed(self, text: str) -> list[float]:
		import hashlib
		h = hashlib.sha256(text.encode("utf-8")).digest()
		arr = [float(b) for b in h[:384]]
		if len(arr) < 384:
			arr = arr + [0.0] * (384 - len(arr))
		n = sum(x * x for x in arr) ** 0.5
		return arr if n == 0 else [x / n for x in arr]
	def upsert(self, ids: List[str], texts: List[str], payloads: List[dict] | None = None):
		vectors = [self.embed(t) for t in texts]
		if self.client:
			points = []
			for i, v in enumerate(vectors):
				pl = {"text": texts[i]}
				if payloads and i < len(payloads):
					pl.update(payloads[i])
				points.append(qmodels.PointStruct(id=ids[i], vector=v, payload=pl))
			self.client.upsert(collection_name=self.collection, points=points)
		else:
			for i, v in enumerate(vectors):
				self.memory_vectors.append((texts[i], v))
				pl = payloads[i] if payloads and i < len(payloads) else {"text": texts[i]}
				self.memory_payloads.append((texts[i], pl))
	def search(self, query: str, limit: int = 5) -> List[Tuple[dict, float]]:
		qv = self.embed(query)
		if self.client:
			res = self.client.search(collection_name=self.collection, query_vector=qv, limit=limit)
			return [(p.payload or {}, p.score) for p in res]
		if not self.memory_vectors:
			return []
		sims = []
		for idx, (t, v) in enumerate(self.memory_vectors):
			score = float(sum(a * b for a, b in zip(qv, v)))
			payload = self.memory_payloads[idx][1] if idx < len(self.memory_payloads) else {"text": t}
			sims.append((payload, score))
		sims.sort(key=lambda x: x[1], reverse=True)
		return sims[:limit]
_default_index: VectorIndex | None = None
def get_index() -> VectorIndex:
	global _default_index
	if _default_index is None:
		_default_index = VectorIndex()
	return _default_index

