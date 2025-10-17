from __future__ import annotations

import logging
from io import BytesIO
from typing import List

try:
    import docx  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    docx = None  # type: ignore

logger = logging.getLogger(__name__)


def extract_docx_blocks(data: bytes) -> tuple[str | None, List[str], List[List[str]]]:
    """Extract title, paragraphs, and tables from DOCX payload."""
    if docx is None:
        raise RuntimeError(
            "python-docx is not installed. Install dependencies from requirements.txt."
        )

    document = docx.Document(BytesIO(data))

    title: str | None = None
    paragraphs: List[str] = []
    table_rows: List[List[str]] = []

    for index, paragraph in enumerate(document.paragraphs):
        text = paragraph.text.strip()
        if not text:
            continue
        if index == 0:
            title = text
        else:
            paragraphs.append(text)

    for table in document.tables:
        for row in table.rows:
            table_rows.append([cell.text.strip() for cell in row.cells])

    return title, paragraphs, table_rows
