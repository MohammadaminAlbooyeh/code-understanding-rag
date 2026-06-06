import hashlib
import os

from backend.utils.config import settings


class CodeEmbedder:
    def __init__(self, model_name: str = "text-embedding-3-small"):
        self.model_name = model_name
        self.embedding_model = None
        self._client = None

        if "text-embedding" in model_name:
            api_key = os.environ.get("OPENAI_API_KEY") or settings.OPENAI_API_KEY
            if api_key:
                from openai import OpenAI
                self._client = OpenAI(api_key=api_key)
                self.embedding_model = model_name
        else:
            try:
                from sentence_transformers import SentenceTransformer
                self.embedding_model = SentenceTransformer(model_name)
            except Exception:
                pass

    def embed(self, code: str) -> list[float]:
        if self._client is not None:
            resp = self._client.embeddings.create(
                input=code, model=self.embedding_model
            )
            return resp.data[0].embedding
        if self.embedding_model is not None:
            return self.embedding_model.encode(code).tolist()
        return self._fallback_embed(code)

    def embed_batch(self, code_chunks: list[str]) -> list[list[float]]:
        if self._client is not None:
            resp = self._client.embeddings.create(
                input=code_chunks, model=self.embedding_model
            )
            sorted_data = sorted(resp.data, key=lambda x: x.index)
            return [d.embedding for d in sorted_data]
        if self.embedding_model is not None:
            return self.embedding_model.encode(code_chunks).tolist()
        return [self._fallback_embed(c) for c in code_chunks]

    def embed_file(self, filepath: str) -> list[float]:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return self.embed(content)

    def _fallback_embed(self, text: str) -> list[float]:
        h = hashlib.sha256(text.encode()).digest()
        return [b / 255.0 for b in h[:16]]
