# Backend

FastAPI service that receives document uploads, extracts structure, and returns JSON matching the PoC schema.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Option A: run from repo root
# cd ../..
# uvicorn backend.main:app --reload
# Option B: run from backend directory
uvicorn main:app --reload
```

### Environment Variables
- `TOKKI_DEBUG` (optional): enable verbose logging for adapters.
- `TESSERACT_CMD` (optional): path to the `tesseract` binary when OCR is enabled.

### Folder Layout
- `main.py` — FastAPI entry point and routing.
- `schemas/` — Pydantic models for request/response payloads.
- `services/` — extraction adapters and orchestration layer.
- `data/` — runtime artifacts (optional) such as SQLite database.
