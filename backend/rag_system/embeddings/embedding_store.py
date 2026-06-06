from backend.utils.config import settings
from backend.vector_store.chroma_store import ChromaStore
from backend.vector_store.faiss_store import FAISSStore
from backend.vector_store.pinecone_store import PineconeStore


class EmbeddingStore:
    def __init__(self, store_type: str = "chroma"):
        self.store_type = store_type
        self.store = self._create_store(store_type)

    def _create_store(self, store_type: str):
        if store_type == "chroma":
            return ChromaStore(persist_directory=settings.CHROMA_PERSIST_DIR)
        elif store_type == "faiss":
            return FAISSStore(dimension=1536)
        elif store_type == "pinecone":
            return PineconeStore(
                api_key=settings.PINECONE_API_KEY if hasattr(settings, "PINECONE_API_KEY") else "",
                environment="us-west-1",
                index_name="code-embeddings",
            )
        else:
            return ChromaStore(persist_directory=settings.CHROMA_PERSIST_DIR)

    def store_embeddings(self, embeddings: list[list[float]], metadata: list[dict]) -> list[str]:
        return self.store.add(embeddings, metadata)

    def get_embeddings(self, ids: list[str]) -> list[list[float]]:
        return []

    def delete_embeddings(self, ids: list[str]) -> None:
        self.store.delete(ids)

    def get_collection_stats(self) -> dict:
        return self.store.get_collection_info()
