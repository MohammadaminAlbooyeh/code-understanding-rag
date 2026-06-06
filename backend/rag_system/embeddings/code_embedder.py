class CodeEmbedder:
    def __init__(self, model_name: str = "text-embedding-3-small"):
        self.model_name = model_name
        self.embedding_model = None

    def embed(self, code: str) -> list[float]:
        pass

    def embed_batch(self, code_chunks: list[str]) -> list[list[float]]:
        pass

    def embed_file(self, filepath: str) -> list[float]:
        pass
