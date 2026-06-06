class Retriever:
    def __init__(self, embedding_store, llm):
        self.embedding_store = embedding_store
        self.llm = llm

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        pass

    def retrieve_with_scores(self, query: str, top_k: int = 5) -> list[tuple[dict, float]]:
        pass

    def retrieve_by_code(self, code: str, top_k: int = 5) -> list[dict]:
        pass
