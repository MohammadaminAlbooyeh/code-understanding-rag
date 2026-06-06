import re
import math
from collections import Counter


class SimilarityMatcher:
    def __init__(self):
        self.similarity_threshold = 0.7

    def _tokenize(self, code: str) -> list[str]:
        return re.findall(r'\w+', code.lower())

    def match(self, code1: str, code2: str) -> float:
        tokens1 = self._tokenize(code1)
        tokens2 = self._tokenize(code2)
        freq1 = Counter(tokens1)
        freq2 = Counter(tokens2)
        all_tokens = set(freq1.keys()) | set(freq2.keys())
        vec1 = [freq1.get(t, 0) for t in all_tokens]
        vec2 = [freq2.get(t, 0) for t in all_tokens]
        return self.cosine_similarity(vec1, vec2)

    def find_similar(self, code: str, codebase: list[str], top_k: int = 5) -> list[dict]:
        scores = []
        for i, candidate in enumerate(codebase):
            score = self.match(code, candidate)
            scores.append({"index": i, "code": candidate, "score": score})
        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]

    def cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def jaccard_similarity(self, code1: str, code2: str) -> float:
        tokens1 = set(self._tokenize(code1))
        tokens2 = set(self._tokenize(code2))
        if not tokens1 and not tokens2:
            return 1.0
        intersection = tokens1 & tokens2
        union = tokens1 | tokens2
        return len(intersection) / len(union)
