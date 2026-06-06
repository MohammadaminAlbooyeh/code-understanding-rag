class EmbeddingStore:
    def __init__(self, store_type: str = "chroma"):
        self.store_type = store_type
        self.store = None

    def store_embeddings(self, embeddings: list[list[float]], metadata: list[dict]) -> None:
        pass

    def get_embeddings(self, ids: list[str]) -> list[list[float]]:
        pass

    def delete_embeddings(self, ids: list[str]) -> None:
        pass

    def get_collection_stats(self) -> dict:
        pass
