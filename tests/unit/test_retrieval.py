import os
import pytest
from unittest.mock import Mock, patch
from backend.rag_system.retrieval.context_builder import ContextBuilder
from backend.rag_system.retrieval.semantic_search import SemanticSearch
from backend.rag_system.embeddings.code_embedder import CodeEmbedder


@pytest.fixture(autouse=True)
def clear_api_keys():
    with patch("backend.utils.config.settings.OPENAI_API_KEY", ""):
        with patch("backend.utils.config.settings.ANTHROPIC_API_KEY", ""):
            with patch("backend.utils.config.settings.GROQ_API_KEY", ""):
                with patch.dict(os.environ, {"OPENAI_API_KEY": "", "ANTHROPIC_API_KEY": "", "GROQ_API_KEY": ""}, clear=False):
                    yield


class TestContextBuilder:
    @pytest.fixture
    def builder(self):
        return ContextBuilder(max_tokens=100)

    def test_build_from_chunks(self, builder):
        chunks = [
            {"metadata": {"text": "def foo(): pass", "start_line": 1, "end_line": 1}},
            {"metadata": {"text": "def bar(): pass", "start_line": 3, "end_line": 3}},
        ]
        context = builder.build(chunks, "test query")
        assert "Chunk 0" in context
        assert "Chunk 1" in context
        assert "def foo()" in context
        assert "def bar()" in context

    def test_build_empty_chunks(self, builder):
        context = builder.build([], "query")
        assert context == ""

    def test_truncate_context(self, builder):
        long_text = "hello world " * 1000
        truncated = builder.truncate_context(long_text)
        assert len(truncated) <= builder.max_tokens * 4 + 3

    def test_truncate_short_context(self, builder):
        text = "short text"
        assert builder.truncate_context(text) == text

    def test_build_with_surrounding(self, builder):
        chunk = {"metadata": {"text": "line5", "start_line": 5, "end_line": 5}}
        code = "\n".join(f"line{i}" for i in range(1, 12))
        context = builder.build_with_surrounding(chunk, code)
        assert "> line5" in context
        assert context.startswith("  ")

    def test_build_multi_file_context(self, builder):
        chunks = [
            {"metadata": {"text": "code_a", "filename": "a.py", "start_line": 1, "end_line": 1, "chunk_index": 0}},
            {"metadata": {"text": "code_b", "filename": "b.py", "start_line": 2, "end_line": 2, "chunk_index": 1}},
        ]
        context = builder.build_multi_file_context(chunks)
        assert "File: a.py" in context
        assert "File: b.py" in context
        assert "code_a" in context
        assert "code_b" in context


class TestSemanticSearch:
    @pytest.fixture
    def search(self):
        embedder = CodeEmbedder()
        retriever = Mock()
        retriever.embedding_store = None
        return SemanticSearch(embedder, retriever)

    def test_search_no_store(self, search):
        results = search.search("test query", top_k=5)
        assert results == []

    def test_hybrid_search_no_store(self, search):
        results = search.hybrid_search("test query", ["keyword"], top_k=5)
        assert isinstance(results, list)
