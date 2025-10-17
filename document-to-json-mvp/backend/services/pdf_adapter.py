from __future__ import annotations

import logging
from io import BytesIO
from typing import List, Tuple

try:
    import pdfplumber  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pdfplumber = None  # type: ignore

try:
    import fitz  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    fitz = None  # type: ignore

from .. import settings
from ..utils import ocr

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

    fitz_document = None
    if fitz is not None:
        try:
            fitz_document = fitz.open(stream=data, filetype="pdf")
        except Exception as exc:  # pragma: no cover
            logger.warning("pdf-fitz-open-failed", exc_info=exc)
            fitz_document = None

    try:
        with pdfplumber.open(BytesIO(data)) as pdf:
            for page_index, page in enumerate(pdf.pages):
                lines = _normalize_lines(page.extract_text())

                if not lines and fitz_document is not None:
                    lines = _extract_text_via_fitz(fitz_document, page_index)

                if not lines and fitz_document is not None and ocr.available():
                    lines = _extract_text_via_ocr(fitz_document, page_index)

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
    finally:
        if fitz_document is not None:
            fitz_document.close()

    return title, paragraphs, tables


def _normalize_lines(text: str | None) -> List[str]:
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]


def _extract_text_via_fitz(document, page_index: int) -> List[str]:
    try:
        page = document.load_page(page_index)
        text = page.get_text("text")
    except Exception as exc:  # pragma: no cover
        logger.warning("pdf-fitz-text-failed", exc_info=exc)
        return []

    return _normalize_lines(text)


def _extract_text_via_ocr(document, page_index: int) -> List[str]:
    if not ocr.available():
        return []
    try:
        page = document.load_page(page_index)
        rotation = getattr(page, "rotation", 0) or 0
        pixmap = None
        if hasattr(fitz, "Matrix"):
            matrix = fitz.Matrix(2, 2)
            if hasattr(matrix, "prerotate"):
                matrix = matrix.prerotate(rotation)
            elif hasattr(matrix, "preRotate"):
                matrix = matrix.preRotate(rotation)  # legacy casing
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
        if pixmap is None:
            pixmap = page.get_pixmap(dpi=400, alpha=False)
        text = ocr.bytes_to_text(pixmap.tobytes("png"))
    except Exception as exc:  # pragma: no cover
        logger.warning("pdf-ocr-read-failed", exc_info=exc)
        return []

    return [line.strip() for line in text.splitlines() if line.strip()]
