from __future__ import annotations

import logging
from io import BytesIO
from typing import Iterable

from PIL import (
    Image,
    ImageFilter,
    ImageOps,
    UnidentifiedImageError,
)

from .. import settings

logger = logging.getLogger(__name__)

try:
    import pytesseract
except Exception as exc:  # pragma: no cover
    pytesseract = None  # type: ignore[assignment]
    logger.warning("pytesseract-import-failed", exc_info=exc)


if settings.TESSERACT_CMD and pytesseract is not None:
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

DEFAULT_CONFIGS = [
    settings.OCR_CONFIG or "--oem 3 --psm 6",
    "--oem 1 --psm 6 -c preserve_interword_spaces=1",
    "--oem 3 --psm 4",
]


def available() -> bool:
    return settings.ENABLE_OCR and pytesseract is not None


def image_to_text(image: Image.Image) -> str:
    if not available():
        return ""

    try:
        base = _preprocess(image)
        candidates = _run_configs(base, DEFAULT_CONFIGS)
        for text in candidates:
            cleaned = text.strip()
            if cleaned:
                return cleaned
        return ""
    except Exception as exc:  # pragma: no cover
        logger.exception("ocr-image-failed", exc_info=exc)
        return ""


def bytes_to_text(blob: bytes) -> str:
    if not available():
        return ""
    try:
        image = Image.open(BytesIO(blob))
        image = ImageOps.exif_transpose(image)
    except UnidentifiedImageError:
        return ""
    except Exception as exc:  # pragma: no cover
        logger.exception("ocr-bytes-open-failed", exc_info=exc)
        return ""

    return image_to_text(image)


def _run_configs(image: Image.Image, configs: Iterable[str]) -> Iterable[str]:
    if pytesseract is None:  # pragma: no cover
        return []
    for cfg in configs:
        try:
            text = pytesseract.image_to_string(
                image,
                lang=settings.OCR_LANGS,
                config=cfg,
            )
            yield text
        except Exception as exc:  # pragma: no cover
            logger.warning("ocr-config-failed", extra={"config": cfg}, exc_info=exc)
            continue


def _preprocess(image: Image.Image) -> Image.Image:
    img = image.convert("RGB")

    if max(img.size) < 1400:
        scale = 1400 / max(img.size)
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size, Image.LANCZOS)

    grey = ImageOps.grayscale(img)
    inverted = ImageOps.invert(grey)
    contrasted = ImageOps.autocontrast(inverted, cutoff=1)
    denoised = contrasted.filter(ImageFilter.MedianFilter(size=3))
    sharpened = denoised.filter(ImageFilter.UnsharpMask(radius=2, percent=180, threshold=2))

    return sharpened
