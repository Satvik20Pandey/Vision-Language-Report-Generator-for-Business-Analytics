# Vision-Language Report Generator

Made by- Satvik Pandey

Live API:

- Base URL: https://vision-language-report-generator-for.onrender.com
- Health: https://vision-language-report-generator-for.onrender.com/health
- Docs: https://vision-language-report-generator-for.onrender.com/docs

Run locally:

```bash
python -m venv .venv
. .venv/bin/activate || .\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Optional env:

```bash
OPENAI_API_KEY=
SKIP_VISION=1
```

API:

- POST `/api/ingest` multipart form `files`: csv and image files
- POST `/api/report` json `{"file_ids":[...],"pdf":true}`
- POST `/api/search` json `{"query":"text","limit":5}`
- GET `/health`
- Swagger: `/docs`

Deployment (Docker):

```bash
docker build -t vl-report .
docker run -p 8000:8000 --env-file .env vl-report
```

Render (Docker):

```yaml
services:
  - type: web
    name: vl-report
    env: docker
    plan: starter
    dockerfilePath: ./Dockerfile
```

Examples:

```bash
curl -F "files=@data.csv" -F "files=@chart.png" http://localhost:8000/api/ingest
curl -X POST -H "Content-Type: application/json" -d "{\"file_ids\":[1,2],\"pdf\":true}" http://localhost:8000/api/report
```

Live examples:

```bash
curl -F "files=@data.csv" -F "files=@chart.png" https://vision-language-report-generator-for.onrender.com/api/ingest
curl -X POST -H "Content-Type: application/json" -d "{\"file_ids\":[1,2],\"pdf\":true}" https://vision-language-report-generator-for.onrender.com/api/report
```

Submission:

- Push code to GitHub (branch `assignment-impl`)
- Ensure live URL in this README
- Include one example request and response JSON in the repo
- Submit GitHub repo link + live API URL

