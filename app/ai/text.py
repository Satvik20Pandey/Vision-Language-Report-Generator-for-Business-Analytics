from typing import List, Tuple
from .vision import caption_images
from ..config import settings
def analyze_csvs(csv_paths: List[str]) -> Tuple[List[Tuple[str, float]], List[str], List[str]]:
	key_metrics = []
	trends = []
	recs = []
	for p in csv_paths:
		try:
			import pandas as pd  # type: ignore
			df = pd.read_csv(p)
			if not df.empty:
				key_metrics.append(("rows", float(len(df))))
				for col in df.select_dtypes(include="number").columns[:3]:
					key_metrics.append((f"{col}_sum", float(df[col].sum())))
					key_metrics.append((f"{col}_mean", float(df[col].mean())))
					if len(df[col]) > 3:
						diff = df[col].iloc[-1] - df[col].iloc[0]
						if diff > 0:
							trends.append(f"{col} increasing")
						elif diff < 0:
							trends.append(f"{col} decreasing")
		except:
			import csv
			with open(p, "r", encoding="utf-8") as f:
				reader = csv.reader(f)
				rows = list(reader)
			if rows:
				key_metrics.append(("rows", float(max(0, len(rows) - 1))))
	for name, val in key_metrics:
		if isinstance(val, float) and val > 0:
			recs.append(f"monitor {name}")
	return key_metrics, trends, list(dict.fromkeys(recs))
def synthesize_report(csv_metrics: List[Tuple[str, float]], trends: List[str], captions: List[str]) -> str:
	try:
		if settings.openai_api_key:
			from langchain_openai import ChatOpenAI
			llm = ChatOpenAI(openai_api_key=settings.openai_api_key, model="gpt-4o-mini")
			parts = []
			parts.append("Key metrics:")
			for k, v in csv_metrics[:10]:
				parts.append(f"{k}:{v}")
			if trends:
				parts.append("Trends:")
				for t in trends[:5]:
					parts.append(t)
			if captions:
				parts.append("Visuals:")
				for c in captions[:5]:
					parts.append(c or "")
			prompt = "\n".join(parts) + "\nGenerate a short business summary."
			return llm.invoke(prompt).content.strip()
	except:
		pass
	parts = []
	if csv_metrics:
		parts.append("Data shows relevant activity across uploaded tables")
	if trends:
		parts.append("Trend insights detected")
	if captions and any(c for c in captions):
		parts.append("Visual content informs context")
	if not parts:
		return "No significant patterns detected"
	return ". ".join(parts)
def build_recommendations(trends: List[str], csv_metrics: List[Tuple[str, float]]) -> List[str]:
	recs = []
	if trends:
		recs.append("review trend drivers")
	if any(v > 0 for _, v in csv_metrics):
		recs.append("focus on high-impact metrics")
	return list(dict.fromkeys(recs))

