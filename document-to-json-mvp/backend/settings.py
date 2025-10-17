from __future__ import annotations

import os


def _truthy(value: str | None) -> bool:
    if value is None:
        return False
    return value.lower() in {"1", "true", "yes", "on"}


ENABLE_OCR: bool = _truthy(os.getenv("TOKKI_ENABLE_OCR"))
TESSERACT_CMD: str | None = os.getenv("TESSERACT_CMD")
OCR_LANGS: str = os.getenv("TOKKI_OCR_LANGS", "eng")
OCR_CONFIG: str | None = os.getenv("TOKKI_OCR_CONFIG")
