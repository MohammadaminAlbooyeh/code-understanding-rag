from backend.models.database import get_db, SessionLocal
from backend.models.code import Code
from backend.models.analysis import Analysis
from backend.models.documentation import Documentation
from backend.models.qa_pair import QAPair
from backend.models.review import Review
from backend.models.embedding import Embedding
from backend.utils.helpers import generate_id, timestamp
from backend.code_analysis.parser.code_parser import CodeParser
from backend.code_analysis.analyzer.complexity_analyzer import ComplexityAnalyzer
from backend.code_analysis.generators.summary_generator import SummaryGenerator
from backend.utils.exceptions import CodeNotFoundError
from backend.rag_system.embeddings.chunk_splitter import ChunkSplitter
from backend.rag_system.embeddings.code_embedder import CodeEmbedder
from backend.rag_system.embeddings.embedding_store import EmbeddingStore

import os
from datetime import datetime, timezone


class IndexingService:
    def __init__(self):
        pass

    def index_code(self, code_id: str) -> bool:
        db = SessionLocal()
        try:
            record = db.query(Code).filter(Code.id == code_id).first()
            if not record:
                raise CodeNotFoundError(f"Code with id {code_id} not found")
            splitter = ChunkSplitter()
            chunks = splitter.split(record.content)
            embedder = CodeEmbedder()
            texts = [c["text"] for c in chunks]
            embeddings = embedder.embed_batch(texts)
            metadata = []
            for i, chunk in enumerate(chunks):
                meta = {
                    "code_id": code_id,
                    "chunk_index": chunk["chunk_index"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "text": chunk["text"],
                }
                metadata.append(meta)
            store = EmbeddingStore()
            vector_ids = store.store_embeddings(embeddings, metadata)
            for i, chunk in enumerate(chunks):
                vid = vector_ids[i] if i < len(vector_ids) else generate_id()
                emb = Embedding(
                    id=generate_id(),
                    code_id=code_id,
                    chunk_index=chunk["chunk_index"],
                    chunk_text=chunk["text"],
                    vector_id=vid,
                    created_at=datetime.now(timezone.utc),
                )
                db.add(emb)
            db.commit()
            return True
        finally:
            db.close()

    def index_directory(self, directory: str) -> list[str]:
        parser = CodeParser()
        parsed_files = parser.parse_directory(directory)
        code_ids = []
        for parsed in parsed_files:
            content = parsed.get("code", "")
            if not content:
                filepath = parsed.get("filepath", "")
                try:
                    with open(filepath, "r") as f:
                        content = f.read()
                except Exception:
                    continue
            filename = os.path.basename(parsed.get("filepath", "unknown"))
            language = parsed.get("language", "unknown")
            db = SessionLocal()
            try:
                code_id = generate_id()
                record = Code(
                    id=code_id,
                    filename=filename,
                    language=language,
                    content=content,
                    size=len(content.encode("utf-8")),
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )
                db.add(record)
                db.commit()
            finally:
                db.close()
            self.index_code(code_id)
            code_ids.append(code_id)
        return code_ids

    def reindex(self, code_id: str) -> bool:
        db = SessionLocal()
        try:
            existing = db.query(Embedding).filter(Embedding.code_id == code_id).all()
            for emb in existing:
                db.delete(emb)
            db.commit()
        finally:
            db.close()
        return self.index_code(code_id)

    def get_index_status(self, code_id: str) -> dict:
        db = SessionLocal()
        try:
            embeddings = db.query(Embedding).filter(Embedding.code_id == code_id).all()
            chunk_count = len(embeddings)
            last_indexed = None
            if embeddings:
                last_indexed = max(e.created_at for e in embeddings)
            return {
                "code_id": code_id,
                "indexed": chunk_count > 0,
                "chunk_count": chunk_count,
                "last_indexed": last_indexed,
            }
        finally:
            db.close()
