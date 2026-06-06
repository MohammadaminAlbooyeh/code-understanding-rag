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
from backend.rag_system.llm.llm_factory import LLMFactory
from backend.rag_system.llm.prompt_manager import PromptManager
from backend.rag_system.chain.documentation_chain import DocumentationChain

from datetime import datetime, timezone


class DocumentationService:
    def __init__(self):
        pass

    def _get_doc_chain(self):
        try:
            factory = LLMFactory()
            llm = factory.create()
            pm = PromptManager()
            return DocumentationChain(llm, pm)
        except Exception:
            return None

    def generate_docs(self, code_id: str, doc_type: str) -> dict:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")
            parser = CodeParser()
            parsed = parser.parse(record.content, record.language)

            chain = self._get_doc_chain()
            if chain:
                if doc_type == "function":
                    content = chain.generate_function_docs(parsed.get("functions", []))
                elif doc_type == "class":
                    content = chain.generate_class_docs(parsed.get("classes", []))
                elif doc_type == "module":
                    content = chain.generate_module_docs(parsed)
                elif doc_type == "api":
                    content = chain.generate_api_docs(parsed)
                else:
                    content = chain.generate_module_docs(parsed)
            else:
                content = f"# {doc_type.capitalize()} Documentation\n\nAuto-generated documentation for {record.filename}."

            doc_id = generate_id()
            doc = Documentation(
                id=doc_id,
                code_id=code_id,
                doc_type=doc_type,
                content=content,
                created_at=datetime.now(timezone.utc),
            )
            db.add(doc)
            db.commit()
            return {
                "id": doc.id,
                "code_id": doc.code_id,
                "doc_type": doc.doc_type,
                "content": doc.content,
                "created_at": doc.created_at,
            }
        finally:
            db.close()

    def get_docs(self, doc_id: str) -> dict:
        db = SessionLocal()
        try:
            record = db.query(Documentation).filter(Documentation.id == doc_id).first()
            if not record:
                raise CodeUnderstandingError(f"Documentation with id {doc_id} not found")
            return {
                "id": record.id,
                "code_id": record.code_id,
                "doc_type": record.doc_type,
                "content": record.content,
                "created_at": record.created_at,
            }
        finally:
            db.close()

    def export_docs(self, doc_id: str, format: str) -> str:
        db = SessionLocal()
        try:
            record = db.query(Documentation).filter(Documentation.id == doc_id).first()
            if not record:
                raise CodeUnderstandingError(f"Documentation with id {doc_id} not found")
            if format == "markdown":
                return record.content
            elif format == "html":
                import markdown
                return markdown.markdown(record.content)
            else:
                return record.content
        finally:
            db.close()

    def generate_readme(self, project_data: dict) -> str:
        chain = self._get_doc_chain()
        if chain:
            try:
                return chain.generate_readme(project_data)
            except Exception:
                pass
        lines = []
        lines.append(f"# {project_data.get('name', 'Project')}")
        lines.append("")
        lines.append(project_data.get("description", ""))
        return "\n".join(lines)
