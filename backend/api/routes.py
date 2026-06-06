from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException

from backend.api.schemas import (
    CodeUploadResponse, AnalysisResponse, DocumentationResponse,
    QARequest, QAResponse, ReviewResponse, RefactorResponse,
    AnalysisRequest, DocGenerateRequest, DocExportRequest,
    ReviewRequest, RefactorRequest, BatchQARequest,
)
from backend.services.code_service import CodeService
from backend.services.analysis_service import AnalysisService
from backend.services.documentation_service import DocumentationService
from backend.services.qa_service import QAService
from backend.services.review_service import ReviewService
from backend.services.refactor_service import RefactorService
from backend.api.dependencies import (
    get_code_service, get_analysis_service, get_documentation_service,
    get_qa_service, get_review_service, get_refactor_service,
)
from backend.utils.exceptions import CodeUnderstandingError

router = APIRouter()


@router.post("/code/upload", response_model=CodeUploadResponse)
async def upload_code(
    file: UploadFile = File(...),
    language: str = Form(...),
    code_service: CodeService = Depends(get_code_service),
):
    content = await file.read()
    code = content.decode("utf-8")
    result = code_service.upload(code, file.filename, language)
    return result


@router.get("/code", response_model=list[CodeUploadResponse])
async def list_code(
    code_service: CodeService = Depends(get_code_service),
):
    return code_service.list_all()


@router.get("/code/{id}", response_model=CodeUploadResponse)
async def get_code(
    id: str,
    code_service: CodeService = Depends(get_code_service),
):
    try:
        return code_service.get(id)
    except CodeUnderstandingError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/code/{id}")
async def delete_code(
    id: str,
    code_service: CodeService = Depends(get_code_service),
):
    code_service.delete(id)
    return {"message": "deleted"}


@router.post("/analysis/parse", response_model=AnalysisResponse)
async def parse_code(
    request: AnalysisRequest,
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    try:
        return analysis_service.parse_code(request.code_id)
    except CodeUnderstandingError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/analysis/complexity", response_model=AnalysisResponse)
async def analyze_complexity(
    request: AnalysisRequest,
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    try:
        return analysis_service.analyze_complexity(request.code_id)
    except CodeUnderstandingError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/analysis/bugs", response_model=AnalysisResponse)
async def detect_bugs(
    request: AnalysisRequest,
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    try:
        return analysis_service.detect_bugs(request.code_id)
    except CodeUnderstandingError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/analysis/security", response_model=AnalysisResponse)
async def security_analysis(
    request: AnalysisRequest,
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    try:
        return analysis_service.security_analysis(request.code_id)
    except CodeUnderstandingError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/analysis/{id}", response_model=AnalysisResponse)
async def get_analysis(
    id: str,
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    try:
        return analysis_service.get_analysis(id)
    except CodeUnderstandingError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/docs/generate", response_model=DocumentationResponse)
async def generate_docs(
    request: DocGenerateRequest,
    documentation_service: DocumentationService = Depends(get_documentation_service),
):
    try:
        return documentation_service.generate_docs(request.code_id, request.doc_type)
    except CodeUnderstandingError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/docs/{id}", response_model=DocumentationResponse)
async def get_docs(
    id: str,
    documentation_service: DocumentationService = Depends(get_documentation_service),
):
    try:
        return documentation_service.get_docs(id)
    except CodeUnderstandingError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/docs/export")
async def export_docs(
    request: DocExportRequest,
    documentation_service: DocumentationService = Depends(get_documentation_service),
):
    try:
        content = documentation_service.export_docs(request.doc_id, request.format)
        return {"content": content, "format": request.format}
    except CodeUnderstandingError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/qa", response_model=QAResponse)
async def ask_question(
    request: QARequest,
    qa_service: QAService = Depends(get_qa_service),
):
    try:
        return qa_service.ask(request.code_id, request.question)
    except CodeUnderstandingError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/qa/history", response_model=list[QAResponse])
async def get_qa_history(
    qa_service: QAService = Depends(get_qa_service),
):
    return qa_service.get_history()


@router.post("/qa/batch", response_model=list[QAResponse])
async def batch_questions(
    request: BatchQARequest,
    qa_service: QAService = Depends(get_qa_service),
):
    questions = [{"code_id": q.code_id, "question": q.question} for q in request.questions]
    return qa_service.batch_ask(questions)


@router.post("/review", response_model=ReviewResponse)
async def code_review(
    request: ReviewRequest,
    review_service: ReviewService = Depends(get_review_service),
):
    try:
        return review_service.review_code(request.code_id)
    except CodeUnderstandingError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/review/{id}", response_model=ReviewResponse)
async def get_review(
    id: str,
    review_service: ReviewService = Depends(get_review_service),
):
    try:
        return review_service.get_review(id)
    except CodeUnderstandingError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/refactor", response_model=RefactorResponse)
async def get_refactoring_suggestions(
    request: RefactorRequest,
    refactor_service: RefactorService = Depends(get_refactor_service),
):
    try:
        suggestions = refactor_service.suggest_refactoring(request.code_id)
        return {
            "id": "",
            "code_id": request.code_id,
            "suggestions": suggestions,
            "created_at": None,
        }
    except CodeUnderstandingError as e:
        raise HTTPException(status_code=404, detail=str(e))
