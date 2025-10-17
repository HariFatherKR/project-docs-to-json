# Document-to-JSON PoC Taskboard

- [ ] Stand up FastAPI project in `document-to-json-mvp/backend/` with health check and `/convert` endpoint accepting PDF/DOCX uploads.
- [ ] Implement extraction adapters: `pdf_adapter.py` (pdfplumber) and `docx_adapter.py` (python-docx) returning unified block models.
- [ ] Draft `JsonDocument` schema (title, headings, paragraphs, tables) and serializer that maps adapter output to PRD JSON format.
- [ ] Persist upload + result logs to SQLite using SQLModel for success tracking.
- [ ] Build Next.js frontend in `document-to-json-mvp/frontend/` providing drag-and-drop upload, progress indicator, JSON viewer, and download button.
- [ ] Add sample documents under `document-to-json-mvp/data/samples/` with expected JSON fixtures; create pytest cases to assert conversions.
- [ ] Integrate OCR fallback (pytesseract) for image-heavy PDFs behind feature flag.
- [ ] Automate `npm run lint`, `pytest`, and integration smoke test via GitHub Actions or local script.
- [ ] Capture MVP demo script and performance checklist (accuracy ≥80%, <5s for ≤10MB files) before stakeholder review.
