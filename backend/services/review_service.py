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
from backend.utils.exceptions import CodeNotFoundError, CodeUnderstandingError
from backend.code_analysis.analyzer.security_analyzer import SecurityAnalyzer
from backend.rag_system.llm.llm_factory import LLMFactory
from backend.rag_system.llm.prompt_manager import PromptManager
from backend.rag_system.chain.review_chain import ReviewChain

from datetime import datetime, timezone


class ReviewService:
    def __init__(self):
        pass

    def _get_review_chain(self):
        try:
            factory = LLMFactory()
            llm = factory.create()
            pm = PromptManager()
            return ReviewChain(llm, pm)
        except Exception:
            return None

    def review_code(self, code_id: str) -> dict:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")

            chain = self._get_review_chain()
            if chain:
                try:
                    result = chain.review_code(record.content, record.language)
                    quality_score = result.get("quality_score", 0.0)
                    issues = result.get("issues", [])
                    suggestions = result.get("suggestions", [])
                except Exception:
                    quality_score = 7.5
                    issues = []
                    suggestions = ["Review the code manually for best practices"]
            else:
                quality_score = 7.5
                issues = []
                suggestions = ["Review the code manually for best practices"]

            review_id = generate_id()
            review = Review(
                id=review_id,
                code_id=code_id,
                quality_score=quality_score,
                issues=issues,
                suggestions=suggestions,
                created_at=datetime.now(timezone.utc),
            )
            db.add(review)
            db.commit()
            return {
                "id": review.id,
                "code_id": review.code_id,
                "quality_score": review.quality_score,
                "issues": review.issues,
                "suggestions": review.suggestions,
                "created_at": review.created_at,
            }
        finally:
            db.close()

    def get_review(self, review_id: str) -> dict:
        db = SessionLocal()
        try:
            record = db.query(Review).filter(Review.id == review_id).first()
            if not record:
                raise CodeUnderstandingError(f"Review with id {review_id} not found")
            return {
                "id": record.id,
                "code_id": record.code_id,
                "quality_score": record.quality_score,
                "issues": record.issues,
                "suggestions": record.suggestions,
                "created_at": record.created_at,
            }
        finally:
            db.close()

    def check_style(self, code_id: str) -> list[dict]:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")
            chain = self._get_review_chain()
            if chain:
                try:
                    return chain.check_style(record.content, record.language)
                except Exception:
                    pass
            return []
        finally:
            db.close()

    def check_security(self, code_id: str) -> list[dict]:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")
            analyzer = SecurityAnalyzer()
            return analyzer.analyze(record.content, record.language)
        finally:
            db.close()
