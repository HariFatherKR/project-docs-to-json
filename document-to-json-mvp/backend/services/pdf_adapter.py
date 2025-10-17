from __future__ import annotations

import logging
from io import BytesIO
from typing import List, Tuple

try:
    import pdfplumber  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pdfplumber = None  # type: ignore

logger = logging.getLogger(__name__)


def extract_pdf_blocks(data: bytes) -> Tuple[str | None, List[str], List[List[str]]]:
    """Extract title, paragraphs, and table-like rows from a PDF payload."""
    if pdfplumber is None:
        raise RuntimeError(
            "pdfplumber is not installed. Install dependencies from requirements.txt."
        )

    title: str | None = None
    paragraphs: List[str] = []
    tables: List[List[str]] = []

    with pdfplumber.open(BytesIO(data)) as pdf:
        for page_index, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            lines = [line.strip() for line in text.splitlines() if line.strip()]

            if page_index == 0 and lines:
                title = lines[0]
                lines = lines[1:]

            paragraphs.extend(lines)

            for table in page.extract_tables() or []:
                flat_rows = [
                    [cell.strip() if isinstance(cell, str) else "" for cell in row]
                    for row in table
                ]
                if flat_rows:
                    tables.extend(flat_rows)

    return title, paragraphs, tables
