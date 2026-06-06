from backend.vector_store.base_store import BaseVectorStore


class ChromaStore(BaseVectorStore):
    def __init__(self, persist_directory: str = "./data/vector_db"):
        self.persist_directory = persist_directory
        self.collection = None

    def add(self, embeddings: list[list[float]], metadata: list[dict]) -> list[str]:
        pass

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        pass

    def delete(self, ids: list[str]) -> None:
        pass

    def get_collection_info(self) -> dict:
        pass
