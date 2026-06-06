from fastapi import Depends
from backend.services.code_service import CodeService
from backend.services.analysis_service import AnalysisService


def get_code_service() -> CodeService:
    return CodeService()


def get_analysis_service() -> AnalysisService:
    return AnalysisService()
