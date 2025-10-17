from __future__ import annotations

import logging
from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .schemas.json_output import ConversionResponse, ErrorResponse
from .services.extractor import SUPPORTED_EXTENSIONS, convert_bytes

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Document-to-JSON Converter",
    description="PoC service that converts PDF/DOCX uploads into structured JSON.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def validate_file(file: UploadFile) -> UploadFile:
    content = file.filename or ""
    suffix = Path(content).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{suffix}'. Upload PDF or DOCX.",
        )
    return file


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/convert",
    response_model=ConversionResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def convert_document(
    file: UploadFile = Depends(validate_file),
) -> JSONResponse:
    payload = await file.read()
    if not payload:
        raise HTTPException(status_code=400, detail="Empty file upload")

    document = convert_bytes(file.filename or "document", payload)

    response = ConversionResponse(document=document, warnings=[])
    return JSONResponse(
        status_code=200,
        content=response.model_dump(mode="json"),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):  # type: ignore[override]
    logger.warning("http-error", extra={"detail": exc.detail, "status": exc.status_code})
    payload = ErrorResponse(detail=str(exc.detail)).model_dump(mode="json")
    return JSONResponse(status_code=exc.status_code, content=payload)
