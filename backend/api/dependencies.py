from fastapi import Depends
from backend.services.code_service import CodeService
from backend.services.analysis_service import AnalysisService
from backend.services.documentation_service import DocumentationService
from backend.services.qa_service import QAService
from backend.services.review_service import ReviewService
from backend.services.refactor_service import RefactorService
from backend.services.indexing_service import IndexingService


def get_code_service() -> CodeService:
    return CodeService()


def get_analysis_service() -> AnalysisService:
    return AnalysisService()


def get_documentation_service() -> DocumentationService:
    return DocumentationService()


def get_qa_service() -> QAService:
    return QAService()


def get_review_service() -> ReviewService:
    return ReviewService()


def get_refactor_service() -> RefactorService:
    return RefactorService()


def get_indexing_service() -> IndexingService:
    return IndexingService()
