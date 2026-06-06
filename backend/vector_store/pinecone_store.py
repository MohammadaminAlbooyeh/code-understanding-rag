from backend.vector_store.base_store import BaseVectorStore


class PineconeStore(BaseVectorStore):
    def __init__(self, api_key: str, environment: str, index_name: str):
        self.api_key = api_key
        self.environment = environment
        self.index_name = index_name
        self.index = None

    def add(self, embeddings: list[list[float]], metadata: list[dict]) -> list[str]:
        pass

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        pass

    def delete(self, ids: list[str]) -> None:
        pass

    def get_collection_info(self) -> dict:
        pass
