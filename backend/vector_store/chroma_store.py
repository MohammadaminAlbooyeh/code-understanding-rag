import uuid
import chromadb
from chromadb.config import Settings

from backend.vector_store.base_store import BaseVectorStore


class ChromaStore(BaseVectorStore):
    def __init__(self, persist_directory: str = "./data/vector_db"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(
            path=persist_directory, settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="code_embeddings"
        )

    def add(self, embeddings: list[list[float]], metadata: list[dict]) -> list[str]:
        ids = [str(uuid.uuid4()) for _ in range(len(embeddings))]
        documents = [m.pop("text", "") if "text" in m else "" for m in metadata]
        self.collection.add(embeddings=embeddings, metadatas=metadata, ids=ids, documents=documents)
        return ids

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding], n_results=top_k
            )
            ids = results["ids"][0]
            metadatas = results["metadatas"][0]
            distances = results.get("distances", [[None] * len(ids)])[0]
            return [
                {"id": id_, "metadata": meta, "score": 1 - dist if dist is not None else None}
                for id_, meta, dist in zip(ids, metadatas, distances)
            ]
        except Exception:
            return []

    def delete(self, ids: list[str]) -> None:
        self.collection.delete(ids=ids)

    def get_collection_info(self) -> dict:
        count = self.collection.count()
        return {
            "count": count,
            "dimension": len(self.collection.peek(1)["embeddings"][0]) if count > 0 else None,
            "name": self.collection.name,
        }
