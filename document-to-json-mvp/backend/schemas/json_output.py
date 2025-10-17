from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class TableRow(BaseModel):
    cells: List[str] = Field(default_factory=list)


class Table(BaseModel):
    headers: List[str] = Field(default_factory=list)
    rows: List[TableRow] = Field(default_factory=list)


class Section(BaseModel):
    heading: Optional[str] = None
    paragraphs: List[str] = Field(default_factory=list)


class JsonDocument(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None
    sections: List[Section] = Field(default_factory=list)
    tables: List[Table] = Field(default_factory=list)
    confidence: float = 0.0


class ConversionResponse(BaseModel):
    document: JsonDocument
    warnings: List[str] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    detail: str
    hints: Optional[List[str]] = None
