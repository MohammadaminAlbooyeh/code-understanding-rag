class Retriever:
    def __init__(self, embedding_store, llm):
        self.embedding_store = embedding_store
        self.llm = llm

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        embedder = getattr(self.embedding_store, "_embedder", None)
        if embedder is None:
            return []
        query_emb = embedder.embed(query)
        return self.embedding_store.store.search(query_emb, top_k)

    def retrieve_with_scores(self, query: str, top_k: int = 5) -> list[tuple[dict, float]]:
        results = self.retrieve(query, top_k)
        return [(r, r.get("score", 0.0)) for r in results]

    def retrieve_by_code(self, code: str, top_k: int = 5) -> list[dict]:
        embedder = getattr(self.embedding_store, "_embedder", None)
        if embedder is None:
            return []
        code_emb = embedder.embed(code)
        return self.embedding_store.store.search(code_emb, top_k)
