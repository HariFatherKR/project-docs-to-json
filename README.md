# Document-to-JSON Converter PoC

Document-to-JSON Converter is a four-week proof of concept that transforms uploaded PDF and DOCX files into a structured JSON schema. The MVP validates Hyto’s ability to auto-extract titles, headings, body copy, and tables with ≥80% accuracy and deliver results through a lightweight web experience.

## Goals
- Provide a drag-and-drop upload UI and preview of generated JSON.
- Build a FastAPI service that orchestrates text extraction, structure detection, and schema formatting.
- Support baseline PDF/DOCX parsing with an OCR fallback plan for scanned documents.
- Log conversions for accuracy tracking and latency metrics (<5 seconds for ≤10 MB files).

## Repository Layout
- `PRD.md` — authoritative product requirements.
- `AGENTS.md` — contributor workflow and coding standards.
- `TASK.md` — current execution board for MVP milestones.
- `document-to-json-mvp/` — application source (backend, frontend, shared assets).

## Tech Overview
- **Backend:** FastAPI, pdfplumber, python-docx, optional Tesseract OCR.
- **Frontend:** Next.js 15 + TypeScript, Tailwind for rapid UI.
- **Storage/Infra:** SQLite for logs (PoC), deployable to Vercel / Fly.io.

## Getting Started
1. Create a virtualenv in `document-to-json-mvp/backend/` and run `pip install -r requirements.txt` (FastAPI, extraction libs).
2. Start the API from the repo root with `uvicorn backend.main:app --reload` (or run `uvicorn main:app --reload` if you stay inside `backend/`).
3. From `document-to-json-mvp/frontend/`, install dependencies via `npm install` and run `npm run dev`.
4. Visit the UI, upload a sample document from `data/samples/`, inspect the preview JSON, and download the result.

Refer to `TASK.md` for the active implementation sequence and testing expectations.
