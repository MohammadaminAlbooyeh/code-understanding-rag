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
from backend.utils.exceptions import CodeNotFoundError, AnalysisNotFoundError
from backend.code_analysis.analyzer.bug_detector import BugDetector
from backend.code_analysis.analyzer.security_analyzer import SecurityAnalyzer
from backend.code_analysis.analyzer.pattern_analyzer import PatternAnalyzer

from datetime import datetime, timezone


class AnalysisService:
    def __init__(self):
        pass

    def parse_code(self, code_id: str) -> dict:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")
            parser = CodeParser()
            parsed = parser.parse(record.content, record.language)
            analysis_id = generate_id()
            analysis = Analysis(
                id=analysis_id,
                code_id=code_id,
                analysis_type="parse",
                results=parsed,
                created_at=datetime.now(timezone.utc),
            )
            db.add(analysis)
            db.commit()
            return {
                "id": analysis.id,
                "code_id": analysis.code_id,
                "analysis_type": analysis.analysis_type,
                "results": analysis.results,
                "created_at": analysis.created_at,
            }
        finally:
            db.close()

    def analyze_complexity(self, code_id: str) -> dict:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")
            analyzer = ComplexityAnalyzer()
            results = analyzer.analyze(record.content, record.language)
            analysis_id = generate_id()
            analysis = Analysis(
                id=analysis_id,
                code_id=code_id,
                analysis_type="complexity",
                results=results,
                created_at=datetime.now(timezone.utc),
            )
            db.add(analysis)
            db.commit()
            return {
                "id": analysis.id,
                "code_id": analysis.code_id,
                "analysis_type": analysis.analysis_type,
                "results": analysis.results,
                "created_at": analysis.created_at,
            }
        finally:
            db.close()

    def detect_bugs(self, code_id: str) -> dict:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")
            detector = BugDetector()
            results = detector.analyze(record.content, record.language)
            analysis_id = generate_id()
            analysis = Analysis(
                id=analysis_id,
                code_id=code_id,
                analysis_type="bugs",
                results={"bugs": results},
                created_at=datetime.now(timezone.utc),
            )
            db.add(analysis)
            db.commit()
            return {
                "id": analysis.id,
                "code_id": analysis.code_id,
                "analysis_type": analysis.analysis_type,
                "results": analysis.results,
                "created_at": analysis.created_at,
            }
        finally:
            db.close()

    def security_analysis(self, code_id: str) -> dict:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")
            analyzer = SecurityAnalyzer()
            results = analyzer.analyze(record.content, record.language)
            analysis_id = generate_id()
            analysis = Analysis(
                id=analysis_id,
                code_id=code_id,
                analysis_type="security",
                results={"vulnerabilities": results},
                created_at=datetime.now(timezone.utc),
            )
            db.add(analysis)
            db.commit()
            return {
                "id": analysis.id,
                "code_id": analysis.code_id,
                "analysis_type": analysis.analysis_type,
                "results": analysis.results,
                "created_at": analysis.created_at,
            }
        finally:
            db.close()

    def analyze_patterns(self, code_id: str) -> dict:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")
            analyzer = PatternAnalyzer()
            results = analyzer.analyze(record.content, record.language)
            analysis_id = generate_id()
            analysis = Analysis(
                id=analysis_id,
                code_id=code_id,
                analysis_type="patterns",
                results=results,
                created_at=datetime.now(timezone.utc),
            )
            db.add(analysis)
            db.commit()
            return {
                "id": analysis.id,
                "code_id": analysis.code_id,
                "analysis_type": analysis.analysis_type,
                "results": analysis.results,
                "created_at": analysis.created_at,
            }
        finally:
            db.close()

    def get_analysis(self, analysis_id: str) -> dict:
        db = SessionLocal()
        try:
            record = db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if not record:
                raise AnalysisNotFoundError(f"Analysis with id {analysis_id} not found")
            return {
                "id": record.id,
                "code_id": record.code_id,
                "analysis_type": record.analysis_type,
                "results": record.results,
                "created_at": record.created_at,
            }
        finally:
            db.close()
