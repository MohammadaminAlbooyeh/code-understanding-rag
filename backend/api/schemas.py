from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


class CodeUploadResponse(BaseModel):
    id: str
    filename: str
    language: str
    size: int
    uploaded_at: datetime


class AnalysisResponse(BaseModel):
    id: str
    code_id: str
    analysis_type: str
    results: dict[str, Any]
    created_at: datetime


class DocumentationResponse(BaseModel):
    id: str
    code_id: str
    doc_type: str
    content: str
    created_at: datetime


class QARequest(BaseModel):
    code_id: str
    question: str
    context: Optional[str] = None


class QAResponse(BaseModel):
    id: str
    code_id: str
    question: str
    answer: str
    sources: list[str]
    created_at: datetime


class ReviewResponse(BaseModel):
    id: str
    code_id: str
    quality_score: float
    issues: list[dict[str, Any]]
    suggestions: list[str]
    created_at: datetime


class RefactorResponse(BaseModel):
    id: str
    code_id: str
    suggestions: list[dict[str, Any]]
    created_at: datetime
