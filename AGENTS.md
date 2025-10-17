# Repository Guidelines

## Scope & Architecture
This repository hosts the Document-to-JSON Converter PoC (see `PRD.md`). MVP delivers a web UI for uploading PDF/DOCX files, a FastAPI service that extracts structure, and JSON output rendered and downloadable client-side. Code lives in `document-to-json-mvp/` with `backend/` (FastAPI, extraction pipeline) and `frontend/` (Next.js UI). Keep infra scripts and shared schemas in `infrastructure/` or `shared/` if introduced. Store sample fixtures under `data/samples/`.

## Setup & Commands
- Backend: `uvicorn backend.main:app --reload` (requires Python 3.11+, dependencies from `backend/requirements.txt`).  
  Run `pytest` for backend unit tests once added.  
- Frontend: `npm install && npm run dev` inside `frontend/` (Next.js 15).  
- Linting: `ruff check backend/` (optional) and `npm run lint` for frontend. Document any new scripts in each package.json or Makefile.

## Coding Standards
Backend uses FastAPI + Pydantic; prefer typed functions, dependency-injected services, and small, pure helpers. Organize extraction logic under `backend/services/` with adapters per file type (PDF, DOCX, OCR). Frontend follows TypeScript strict mode, functional React components, and hooks for API calls. Shared schemas (`schemas/json_output.py`) define the canonical JSON contract; frontend should reference the generated TypeScript types (e.g., via `ts-json-schema-generator`).

## Testing & QA
Create deterministic fixtures in `data/samples/` covering headings, tables, and OCR edge cases. Backend tests should assert parser output matches the target JSON schema and measure confidence scores. Frontend tests can begin with Playwright smoke flows (upload → preview → download). Before each PR, verify `uvicorn` logs, `pytest`, and `npm run lint`. Aim for 80% coverage on critical parsing modules per PRD success metrics.

## Collaboration Workflow
Use Conventional Commits (`feat:`, `fix:`, `chore:`). Every PR must link to a task in `TASK.md`, describe input formats handled, and attach JSON diffs and screenshots/GIFs of the upload flow. Require at least one reviewer for pipeline changes. Update localization or schema docs when fields change, and bump API version if breaking.
