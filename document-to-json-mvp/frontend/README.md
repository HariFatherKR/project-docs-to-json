# Frontend

Next.js UI for the Document-to-JSON Converter PoC.

## Development

```bash
npm install
npm run dev
```

Set `NEXT_PUBLIC_API_BASE` in `.env.local` if the FastAPI service runs on a non-default host.

## Features
+- Drag-and-drop upload for PDF/DOCX.
+- Progress feedback while the backend converts the file.
+- JSON preview panel with download button.
