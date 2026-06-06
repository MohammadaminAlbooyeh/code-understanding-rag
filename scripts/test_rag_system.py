import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.rag_system.embeddings.chunk_splitter import ChunkSplitter
from backend.rag_system.embeddings.code_embedder import CodeEmbedder
from backend.rag_system.retrieval.similarity_matcher import SimilarityMatcher
from backend.rag_system.retrieval.context_builder import ContextBuilder


def main():
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b
"""

    sample_code2 = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


class MathUtils:
    def square(self, x):
        return x * x
"""

    print("=== ChunkSplitter Test ===")
    splitter = ChunkSplitter(chunk_size=200, chunk_overlap=50)
    chunks = splitter.split(sample_code)
    print(f"  Chunks created: {len(chunks)}")
    for c in chunks:
        print(f"    Chunk {c['chunk_index']}: lines {c['start_line']}-{c['end_line']} ({len(c['text'])} chars)")

    print()
    print("=== CodeEmbedder Test ===")
    embedder = CodeEmbedder()
    try:
        embedding = embedder.embed(sample_code)
        print(f"  Live embedder succeeded: dimension {len(embedding)}")
        print(f"  Embedding (first 5 values): {embedding[:5]}")
    except Exception as e:
        print(f"  Live embedder unavailable ({e})")

    print("  Demonstrating fallback embedding...")
    fallback = CodeEmbedder()._fallback_embed(sample_code)
    print(f"  Fallback embedding dimension: {len(fallback)}")
    print(f"  Fallback embedding (first 5 values): {fallback[:5]}")

    print()
    print("=== SimilarityMatcher Test ===")
    matcher = SimilarityMatcher()
    similarity = matcher.match(sample_code, sample_code2)
    print(f"  Cosine similarity: {similarity:.4f}")

    codebase = [
        "def foo(): pass",
        sample_code2,
        "x = 1",
    ]
    similar = matcher.find_similar(sample_code, codebase, top_k=2)
    print(f"  Top matches:")
    for s in similar:
        print(f"    Score {s['score']:.4f}: {s['code'][:50]}...")

    print()
    print("=== ContextBuilder Test ===")
    builder = ContextBuilder(max_tokens=500)
    context = builder.build(chunks, "fibonacci")
    print(f"  Context length: {len(context)} chars")
    print(f"  Context preview: {context[:120]}...")

    print()
    print("RAG system test complete.")


if __name__ == "__main__":
    main()
