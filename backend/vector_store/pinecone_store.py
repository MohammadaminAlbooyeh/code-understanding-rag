import uuid

from backend.vector_store.base_store import BaseVectorStore

try:
    from pinecone import Pinecone, ServerlessSpec
    _PINECONE_AVAILABLE = True
except ImportError:
    Pinecone = None
    ServerlessSpec = None
    _PINECONE_AVAILABLE = False


class PineconeStore(BaseVectorStore):
    def __init__(self, api_key: str, environment: str, index_name: str):
        self.api_key = api_key
        self.environment = environment
        self.index_name = index_name
        if not _PINECONE_AVAILABLE:
            raise ImportError("pinecone is not installed. Run: pip install pinecone")
        self.pc = Pinecone(api_key=api_key)
        existing = [idx["name"] for idx in self.pc.list_indexes()]
        if index_name not in existing:
            self.pc.create_index(
                name=index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=environment),
            )
        self.index = self.pc.Index(index_name)

    def add(self, embeddings: list[list[float]], metadata: list[dict]) -> list[str]:
        ids = [str(uuid.uuid4()) for _ in range(len(embeddings))]
        vectors = list(zip(ids, embeddings, metadata))
        self.index.upsert(vectors=vectors)
        return ids

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        try:
            results = self.index.query(
                vector=query_embedding, top_k=top_k, include_metadata=True
            )
            return [
                {
                    "id": match["id"],
                    "metadata": match["metadata"],
                    "score": match["score"],
                }
                for match in results["matches"]
            ]
        except Exception:
            return []

    def delete(self, ids: list[str]) -> None:
        self.index.delete(ids=ids)

    def get_collection_info(self) -> dict:
        stats = self.index.describe_index_stats()
        return {
            "name": self.index_name,
            "dimension": stats["dimension"],
            "total_count": stats["total_vector_count"],
            "namespaces": stats["namespaces"],
        }
