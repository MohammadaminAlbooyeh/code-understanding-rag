from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


class CodeUploadRequest(BaseModel):
    code: str
    filename: str
    language: str


class CodeUploadResponse(BaseModel):
    id: str
    filename: str
    language: str
    size: int
    uploaded_at: datetime


class AnalysisRequest(BaseModel):
    code_id: str


class AnalysisResponse(BaseModel):
    id: str
    code_id: str
    analysis_type: str
    results: dict[str, Any]
    created_at: datetime


class DocGenerateRequest(BaseModel):
    code_id: str
    doc_type: str


class DocExportRequest(BaseModel):
    doc_id: str
    format: str


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


class BatchQARequest(BaseModel):
    questions: list[QARequest]


class ReviewRequest(BaseModel):
    code_id: str


class ReviewResponse(BaseModel):
    id: str
    code_id: str
    quality_score: float
    issues: list[dict[str, Any]]
    suggestions: list[str]
    created_at: datetime


class RefactorRequest(BaseModel):
    code_id: str


class RefactorResponse(BaseModel):
    id: str
    code_id: str
    suggestions: list[dict[str, Any]]
    created_at: datetime
