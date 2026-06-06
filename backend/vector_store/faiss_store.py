import uuid
import numpy as np
import faiss

from backend.vector_store.base_store import BaseVectorStore


class FAISSStore(BaseVectorStore):
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.metadata_store: list[dict] = []
        self.active_ids: list[str] = []

    def add(self, embeddings: list[list[float]], metadata: list[dict]) -> list[str]:
        ids = [str(uuid.uuid4()) for _ in range(len(embeddings))]
        vectors = np.array(embeddings, dtype=np.float32)
        self.index.add(vectors)
        self.metadata_store.extend(metadata)
        self.active_ids.extend(ids)
        return ids

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        if self.index.ntotal == 0:
            return []
        query = np.array([query_embedding], dtype=np.float32)
        distances, indices = self.index.search(query, min(top_k, self.index.ntotal))
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(self.active_ids):
                continue
            results.append({
                "id": self.active_ids[idx],
                "metadata": self.metadata_store[idx],
                "score": float(dist),
            })
        return results

    def delete(self, ids: list[str]) -> None:
        ids_to_remove = set(ids)
        surviving = [
            (aid, meta)
            for aid, meta in zip(self.active_ids, self.metadata_store)
            if aid not in ids_to_remove
        ]
        if surviving:
            self.active_ids, self.metadata_store = zip(*surviving)
            self.active_ids = list(self.active_ids)
            self.metadata_store = list(self.metadata_store)
        else:
            self.active_ids = []
            self.metadata_store = []
        if self.active_ids:
            self.index = faiss.IndexFlatIP(self.dimension)
            embeddings = [
                self.metadata_store[i].get("_embedding")
                for i in range(len(self.active_ids))
            ]
            if embeddings[0] is not None:
                vectors = np.array(embeddings, dtype=np.float32)
                self.index.add(vectors)

    def get_collection_info(self) -> dict:
        return {
            "dimension": self.dimension,
            "total_count": self.index.ntotal,
            "is_trained": self.index.is_trained,
        }
