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
- `TOKKI_ENABLE_OCR` (optional): set to `1/true` to enable OCR fallback for image-only content.
- `TOKKI_OCR_LANGS` (optional): comma-separated Tesseract language codes (default `eng`).
- `TOKKI_OCR_CONFIG` (optional): 추가 tesserract 옵션 (예: `--oem 3 --psm 6`).
- `TESSERACT_CMD` (optional): path to the `tesseract` binary when OCR is enabled.

> macOS: `brew install tesseract` 후 `export TESSERACT_CMD=/opt/homebrew/bin/tesseract`처럼 경로를 지정하세요.

### Folder Layout
- `main.py` — FastAPI entry point and routing.
- `schemas/` — Pydantic models for request/response payloads.
- `services/` — extraction adapters and orchestration layer.
- `data/` — runtime artifacts (optional) such as SQLite database.
