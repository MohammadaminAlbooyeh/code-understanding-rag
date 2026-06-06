import os
import pytest
from unittest.mock import patch
from backend.rag_system.embeddings.chunk_splitter import ChunkSplitter
from backend.rag_system.embeddings.code_embedder import CodeEmbedder
from backend.rag_system.retrieval.similarity_matcher import SimilarityMatcher


@pytest.fixture(autouse=True)
def clear_api_keys():
    with patch("backend.utils.config.settings.OPENAI_API_KEY", ""):
        with patch("backend.utils.config.settings.ANTHROPIC_API_KEY", ""):
            with patch("backend.utils.config.settings.GROQ_API_KEY", ""):
                with patch.dict(os.environ, {"OPENAI_API_KEY": "", "ANTHROPIC_API_KEY": "", "GROQ_API_KEY": ""}, clear=False):
                    yield


class TestChunkSplitter:
    @pytest.fixture
    def splitter(self):
        return ChunkSplitter(chunk_size=50, chunk_overlap=10)

    def test_basic_character_split(self, splitter):
        code = "a" * 200
        chunks = splitter.split(code)
        assert len(chunks) > 1
        assert all("text" in c for c in chunks)
        assert all("start_line" in c for c in chunks)
        assert all("end_line" in c for c in chunks)
        assert all("chunk_index" in c for c in chunks)

    def test_split_small_code(self):
        splitter = ChunkSplitter(chunk_size=1000, chunk_overlap=200)
        code = "def foo():\n    pass\n"
        chunks = splitter.split(code)
        assert len(chunks) == 1
        assert chunks[0]["text"] == code

    def test_total_chunks_set(self, splitter):
        code = "line1\nline2\nline3\n"
        chunks = splitter.split(code)
        for c in chunks:
            assert c["total_chunks"] == len(chunks)

    def test_split_by_function(self):
        splitter = ChunkSplitter()
        parsed = {
            "functions": [
                {"name": "foo", "start_line": 1, "end_line": 3},
                {"name": "bar", "start_line": 5, "end_line": 7},
            ],
            "code": "def foo():\n    pass\n\ndef bar():\n    pass\n",
        }
        chunks = splitter.split_by_function(parsed)
        assert len(chunks) == 2
        assert chunks[0]["function_name"] == "foo"
        assert chunks[1]["function_name"] == "bar"
        assert all("text" in c for c in chunks)

    def test_split_by_class(self):
        splitter = ChunkSplitter()
        parsed = {
            "classes": [
                {"name": "MyClass", "start_line": 1, "end_line": 5},
            ],
            "code": "class MyClass:\n    def method(self):\n        pass\n",
        }
        chunks = splitter.split_by_class(parsed)
        assert len(chunks) == 1
        assert chunks[0]["class_name"] == "MyClass"

    def test_split_by_lines(self):
        splitter = ChunkSplitter()
        lines = "\n".join(f"line{i}" for i in range(100))
        chunks = splitter.split_by_lines(lines, lines_per_chunk=30)
        assert len(chunks) == 4
        assert chunks[0]["start_line"] == 1
        assert chunks[0]["end_line"] == 30
        assert chunks[1]["start_line"] == 31

    def test_split_by_lines_exact_multiple(self):
        splitter = ChunkSplitter()
        lines = "\n".join(f"line{i}" for i in range(50))
        chunks = splitter.split_by_lines(lines, lines_per_chunk=10)
        assert len(chunks) == 5


class TestCodeEmbedder:
    def test_fallback_embed(self):
        embedder = CodeEmbedder()
        result = embedder.embed("def foo():\n    pass\n")
        assert len(result) == 16
        assert all(isinstance(v, float) for v in result)

    def test_fallback_embed_deterministic(self):
        embedder = CodeEmbedder()
        code = "x = 1"
        r1 = embedder.embed(code)
        r2 = embedder.embed(code)
        assert r1 == r2

    def test_fallback_embed_different_inputs(self):
        embedder = CodeEmbedder()
        r1 = embedder.embed("hello world")
        r2 = embedder.embed("goodbye world")
        assert r1 != r2

    def test_embed_batch(self):
        embedder = CodeEmbedder()
        results = embedder.embed_batch(["def foo(): pass", "def bar(): pass"])
        assert len(results) == 2
        for r in results:
            assert len(r) == 16


class TestSimilarityMatcher:
    @pytest.fixture
    def matcher(self):
        return SimilarityMatcher()

    def test_cosine_similarity_identical(self, matcher):
        assert matcher.cosine_similarity([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)

    def test_cosine_similarity_orthogonal(self, matcher):
        assert matcher.cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)

    def test_cosine_similarity_zero_vector(self, matcher):
        assert matcher.cosine_similarity([0, 0], [1, 2]) == pytest.approx(0.0)

    def test_jaccard_similarity_identical(self, matcher):
        sim = matcher.jaccard_similarity("def foo(): pass", "def foo(): pass")
        assert sim == pytest.approx(1.0)

    def test_jaccard_similarity_different(self, matcher):
        sim = matcher.jaccard_similarity("def foo(): pass", "class Bar: pass")
        assert sim < 1.0

    def test_jaccard_similarity_empty(self, matcher):
        sim = matcher.jaccard_similarity("", "")
        assert sim == pytest.approx(1.0)

    def test_match_identical(self, matcher):
        code = "def hello():\n    return 'world'\n"
        assert matcher.match(code, code) == pytest.approx(1.0)

    def test_match_different(self, matcher):
        sim = matcher.match("def foo(): pass", "class Bar: pass")
        assert sim < 1.0

    def test_find_similar(self, matcher):
        target = "def hello():\n    return 'world'\n"
        candidates = [
            "def hello():\n    return 'world'\n",
            "class Foo:\n    pass\n",
            "x = 1\n",
        ]
        results = matcher.find_similar(target, candidates, top_k=2)
        assert len(results) == 2
        assert results[0]["index"] == 0
        assert results[0]["score"] == pytest.approx(1.0)
