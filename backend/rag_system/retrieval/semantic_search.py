class SemanticSearch:
    def __init__(self, embedder, retriever):
        self.embedder = embedder
        self.retriever = retriever

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        query_emb = self.embedder.embed(query)
        store = getattr(self.retriever, "embedding_store", None)
        if store is None:
            return []
        return store.store.search(query_emb, top_k)

    def hybrid_search(self, query: str, keywords: list[str], top_k: int = 5) -> list[dict]:
        semantic_results = self.search(query, top_k)
        seen_ids = set()
        merged = []
        for r in semantic_results:
            rid = r.get("id")
            if rid not in seen_ids:
                seen_ids.add(rid)
                merged.append(r)

        keyword_hits = []
        if keywords:
            for r in semantic_results:
                text = str(r.get("metadata", {}).get("text", "")).lower()
                score_boost = sum(1 for kw in keywords if kw.lower() in text)
                if score_boost > 0:
                    keyword_hits.append((r, score_boost))

            keyword_hits.sort(key=lambda x: x[1], reverse=True)
            for r, _ in keyword_hits:
                rid = r.get("id")
                if rid not in seen_ids:
                    seen_ids.add(rid)
                    merged.append(r)

        return merged[:top_k]

    def search_by_example(self, code: str, top_k: int = 5) -> list[dict]:
        return self.retriever.retrieve_by_code(code, top_k)
