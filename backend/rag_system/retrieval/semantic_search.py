class SemanticSearch:
    def __init__(self, embedder, retriever):
        self.embedder = embedder
        self.retriever = retriever

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        pass

    def hybrid_search(self, query: str, keywords: list[str], top_k: int = 5) -> list[dict]:
        pass

    def search_by_example(self, code: str, top_k: int = 5) -> list[dict]:
        pass
