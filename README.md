# Vision-Language Report Generator

Run locally:

```bash
python -m venv .venv
. .venv/bin/activate || .\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Env variables:

```bash
DATABASE_URL=postgresql+psycopg://user:pass@host:5432/dbname
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
S3_BUCKET=
QDRANT_URL=
QDRANT_API_KEY=
OPENAI_API_KEY=
REPORT_FONT=
```

API:

- POST `/api/ingest` multipart form `files`: csv and image files
- POST `/api/report` json `{"file_ids":[...],"pdf":true}`
- GET `/health`
- Swagger: `/docs`

Deployment (Docker):

```bash
docker build -t vl-report .
docker run -p 8000:8000 --env-file .env vl-report
```

Render:

```yaml
services:
  - type: web
    name: vl-report
    env: python
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port 10000
    envVars:
      - key: PORT
        value: 10000
```

Example:

```bash
curl -F "files=@data.csv" -F "files=@chart.png" http://localhost:8000/api/ingest
curl -X POST -H "Content-Type: application/json" -d "{\"file_ids\":[1,2],\"pdf\":true}" http://localhost:8000/api/report
```

