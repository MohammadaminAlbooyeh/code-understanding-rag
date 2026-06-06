from backend.models.database import get_db, SessionLocal
from backend.models.code import Code
from backend.models.analysis import Analysis
from backend.models.documentation import Documentation
from backend.models.qa_pair import QAPair
from backend.models.review import Review
from backend.utils.helpers import generate_id, timestamp
from backend.code_analysis.parser.code_parser import CodeParser
from backend.code_analysis.analyzer.complexity_analyzer import ComplexityAnalyzer
from backend.code_analysis.generators.summary_generator import SummaryGenerator
from backend.utils.exceptions import CodeNotFoundError
from backend.rag_system.llm.llm_factory import LLMFactory
from backend.rag_system.llm.prompt_manager import PromptManager
from backend.rag_system.chain.refactor_chain import RefactorChain

from datetime import datetime


class RefactorService:
    def __init__(self):
        pass

    def _get_refactor_chain(self):
        try:
            factory = LLMFactory()
            llm = factory.create()
            pm = PromptManager()
            return RefactorChain(llm, pm)
        except Exception:
            return None

    def suggest_refactoring(self, code_id: str) -> list[dict]:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")
            chain = self._get_refactor_chain()
            if chain:
                try:
                    return chain.suggest_refactoring(record.content, record.language)
                except Exception:
                    pass
            return [
                {
                    "type": "refactoring",
                    "description": f"Consider refactoring {record.filename}",
                    "suggestion": "Review code structure for improvements",
                }
            ]
        finally:
            db.close()

    def suggest_optimizations(self, code_id: str) -> list[dict]:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")
            chain = self._get_refactor_chain()
            if chain:
                try:
                    return chain.suggest_optimizations(record.content, record.language)
                except Exception:
                    pass
            return [
                {
                    "type": "optimization",
                    "description": f"Consider optimizing {record.filename}",
                    "suggestion": "Profile the code to identify bottlenecks",
                }
            ]
        finally:
            db.close()

    def apply_refactoring(self, code_id: str, suggestion_id: str) -> str:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")
            suggestions = [
                {
                    "id": suggestion_id,
                    "description": "Apply suggested refactoring",
                }
            ]
            chain = self._get_refactor_chain()
            if chain:
                try:
                    return chain.generate_refactored_code(record.content, suggestions)
                except Exception:
                    pass
            return record.content
        finally:
            db.close()
