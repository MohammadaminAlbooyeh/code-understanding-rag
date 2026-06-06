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
from backend.rag_system.chain.rag_chain import RAGChain
from backend.rag_system.retrieval.retriever import Retriever
from backend.rag_system.embeddings.embedding_store import EmbeddingStore
from backend.rag_system.embeddings.code_embedder import CodeEmbedder

from datetime import datetime, timezone
import json


class QAService:
    def __init__(self):
        pass

    def _get_rag_chain(self):
        try:
            factory = LLMFactory()
            llm = factory.create()
            pm = PromptManager()
            embed_store = EmbeddingStore()
            retriever = Retriever(embed_store, llm)
            return RAGChain(retriever, llm, pm)
        except Exception:
            return None

    def ask(self, code_id: str, question: str) -> dict:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")

            chain = self._get_rag_chain()
            if chain:
                try:
                    answer = chain.run(question, code_id=code_id)
                except Exception:
                    answer = f"Analysis of '{record.filename}' regarding: {question}"
            else:
                answer = f"Analysis of '{record.filename}' regarding: {question}"

            sources = []
            qa_id = generate_id()
            qa = QAPair(
                id=qa_id,
                code_id=code_id,
                question=question,
                answer=answer,
                sources=json.dumps(sources) if sources else "",
                created_at=datetime.now(timezone.utc),
            )
            db.add(qa)
            db.commit()
            return {
                "id": qa.id,
                "code_id": qa.code_id,
                "question": qa.question,
                "answer": qa.answer,
                "sources": sources,
                "created_at": qa.created_at,
            }
        finally:
            db.close()

    def get_history(self) -> list[dict]:
        db = SessionLocal()
        try:
            records = db.query(QAPair).order_by(QAPair.created_at.desc()).all()
            results = []
            for r in records:
                try:
                    sources = json.loads(r.sources) if r.sources else []
                except (json.JSONDecodeError, TypeError):
                    sources = []
                results.append({
                    "id": r.id,
                    "code_id": r.code_id,
                    "question": r.question,
                    "answer": r.answer,
                    "sources": sources,
                    "created_at": r.created_at,
                })
            return results
        finally:
            db.close()

    def batch_ask(self, questions: list[dict]) -> list[dict]:
        results = []
        for item in questions:
            result = self.ask(item["code_id"], item["question"])
            results.append(result)
        return results

    def clear_history(self) -> None:
        db = SessionLocal()
        try:
            db.query(QAPair).delete()
            db.commit()
        finally:
            db.close()
