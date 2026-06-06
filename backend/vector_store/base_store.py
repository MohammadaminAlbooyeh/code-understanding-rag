from abc import ABC, abstractmethod


class BaseVectorStore(ABC):
    @abstractmethod
    def add(self, embeddings: list[list[float]], metadata: list[dict]) -> list[str]:
        pass

    @abstractmethod
    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        pass

    @abstractmethod
    def delete(self, ids: list[str]) -> None:
        pass

    @abstractmethod
    def get_collection_info(self) -> dict:
        pass
