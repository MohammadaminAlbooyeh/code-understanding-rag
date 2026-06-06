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

from datetime import datetime, timezone


class CodeService:
    def __init__(self):
        pass

    def upload(self, code: str, filename: str, language: str) -> dict:
        parser = CodeParser()
        parsed = parser.parse(code, language)
        db = SessionLocal()
        try:
            code_id = generate_id()
            record = Code(
                id=code_id,
                filename=filename,
                language=language,
                content=code,
                size=len(code.encode("utf-8")),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            db.add(record)
            db.commit()
            return {
                "id": code_id,
                "filename": filename,
                "language": language,
                "size": len(code.encode("utf-8")),
                "uploaded_at": record.created_at,
            }
        finally:
            db.close()

    def get(self, code_id: str) -> dict:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")
            return {
                "id": record.id,
                "filename": record.filename,
                "language": record.language,
                "size": record.size,
                "uploaded_at": record.created_at,
                "content": record.content,
            }
        finally:
            db.close()

    def list_all(self) -> list[dict]:
        db = SessionLocal()
        try:
            records = db.query(Code).all()
            return [
                {
                    "id": r.id,
                    "filename": r.filename,
                    "language": r.language,
                    "size": r.size,
                    "uploaded_at": r.created_at,
                }
                for r in records
            ]
        finally:
            db.close()

    def delete(self, code_id: str) -> bool:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if record:
                db.delete(record)
                db.commit()
            return True
        finally:
            db.close()

    def get_languages(self) -> list[str]:
        db = SessionLocal()
        try:
            results = db.query(Code.language).distinct().all()
            return [r[0] for r in results]
        finally:
            db.close()
