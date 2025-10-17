from __future__ import annotations

import datetime as dt
import logging
import os
from typing import List

from fastapi import HTTPException

from ..schemas.json_output import JsonDocument, Section, Table, TableRow
from .docx_adapter import extract_docx_blocks
from .pdf_adapter import extract_pdf_blocks

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def infer_extension(filename: str) -> str:
    lower = filename.lower()
    for ext in SUPPORTED_EXTENSIONS:
        if lower.endswith(ext):
            return ext
    return ""


def build_sections(paragraphs: List[str]) -> List[Section]:
    sections: List[Section] = []
    current = Section(heading=None, paragraphs=[])

    for paragraph in paragraphs:
        if paragraph.isupper() or paragraph.endswith(":"):
            if current.paragraphs:
                sections.append(current)
                current = Section(heading=None, paragraphs=[])
            current.heading = paragraph.rstrip(":")
        else:
            current.paragraphs.append(paragraph)
    if current.heading or current.paragraphs:
        sections.append(current)
    return sections


def build_tables(raw_rows: List[List[str]]) -> List[Table]:
    if not raw_rows:
        return []
    headers: List[str] = raw_rows[0]
    rows = [TableRow(cells=row) for row in raw_rows[1:]]
    return [Table(headers=headers, rows=rows)]


def convert_bytes(filename: str, payload: bytes) -> JsonDocument:
    ext = infer_extension(filename)
    if not ext:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        if ext == ".pdf":
            title, paragraphs, table_rows = extract_pdf_blocks(payload)
        elif ext == ".docx":
            title, paragraphs, table_rows = extract_docx_blocks(payload)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    except RuntimeError as exc:
        logger.exception("adapter-missing-dependency")
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
    except Exception as exc:  # pragma: no cover - fallback
        logger.exception("adapter-failure", extra={"filename": filename})
        raise HTTPException(
            status_code=500,
            detail="Failed to process document",
        ) from exc

    sections = build_sections(paragraphs)
    tables = build_tables(table_rows)

    document = JsonDocument(
        title=title,
        date=dt.date.today().isoformat(),
        sections=sections,
        tables=tables,
        confidence=0.5 if sections or tables else 0.0,
    )

    return document
