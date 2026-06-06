import pytest
from backend.rag_system.embeddings.code_embedder import CodeEmbedder


def test_embed():
    embedder = CodeEmbedder()
    code = "def foo():\n    pass\n"
    result = embedder.embed(code)
    assert result is not None
