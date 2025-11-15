from typing import List, Tuple, Optional
from .schemas import ReportJSON
def build_report_json(summary: str, metrics: List[Tuple[str, float]], trends: List[str], recs: List[str], captions: List[str]) -> ReportJSON:
	return ReportJSON(summary=summary, key_metrics=[{"name": k, "value": v} for k, v in metrics], trends=trends, recommendations=recs, visual_insights=[c for c in captions if c])
def build_pdf(path: str, report: ReportJSON, font: Optional[str] = None):
	try:
		from reportlab.lib.pagesizes import A4
		from reportlab.pdfgen import canvas
		from reportlab.lib.units import cm
	except:
		return
	c = canvas.Canvas(path, pagesize=A4)
	w, h = A4
	y = h - 2 * cm
	if font:
		c.setFont(font, 14)
	else:
		c.setFont("Helvetica-Bold", 14)
	c.drawString(2 * cm, y, "Business Summary Report")
	y -= 1 * cm
	c.setFont("Helvetica", 11)
	for line in [report.summary]:
		c.drawString(2 * cm, y, line[:120])
		y -= 0.8 * cm
	if report.key_metrics:
		c.setFont("Helvetica-Bold", 12)
		c.drawString(2 * cm, y, "Key Metrics")
		y -= 0.8 * cm
		c.setFont("Helvetica", 11)
		for item in report.key_metrics[:10]:
			c.drawString(2 * cm, y, f"{item.name}: {item.value}")
			y -= 0.6 * cm
	if report.trends:
		c.setFont("Helvetica-Bold", 12)
		c.drawString(2 * cm, y, "Trends")
		y -= 0.8 * cm
		c.setFont("Helvetica", 11)
		for t in report.trends[:10]:
			c.drawString(2 * cm, y, t[:120])
			y -= 0.6 * cm
	if report.recommendations:
		c.setFont("Helvetica-Bold", 12)
		c.drawString(2 * cm, y, "Recommendations")
		y -= 0.8 * cm
		c.setFont("Helvetica", 11)
		for r in report.recommendations[:10]:
			c.drawString(2 * cm, y, r[:120])
			y -= 0.6 * cm
	if report.visual_insights:
		c.setFont("Helvetica-Bold", 12)
		c.drawString(2 * cm, y, "Visual Insights")
		y -= 0.8 * cm
		c.setFont("Helvetica", 11)
		for v in report.visual_insights[:10]:
			c.drawString(2 * cm, y, v[:120])
			y -= 0.6 * cm
	c.showPage()
	c.save()

