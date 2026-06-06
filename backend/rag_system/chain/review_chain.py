import re

from backend.rag_system.prompts.review_prompts import (
    CODE_REVIEW_PROMPT,
    STYLE_CHECK_PROMPT,
    BEST_PRACTICES_PROMPT,
)


class ReviewChain:
    def __init__(self, llm, prompt_manager):
        self.llm = llm
        self.prompt_manager = prompt_manager

    def review_code(self, code: str, language: str) -> dict:
        prompt = f"{CODE_REVIEW_PROMPT}\n\nLanguage: {language}\n\nCode:\n{code}"
        response = self.llm.generate(prompt)
        return {"review": response, "language": language}

    def check_style(self, code: str, language: str) -> list[dict]:
        prompt = f"{STYLE_CHECK_PROMPT}\n\nLanguage: {language}\n\nCode:\n{code}"
        response = self.llm.generate(prompt)
        return [{"issue": line.strip()} for line in response.split("\n") if line.strip()]

    def check_best_practices(self, code: str, language: str) -> list[dict]:
        prompt = f"{BEST_PRACTICES_PROMPT}\n\nLanguage: {language}\n\nCode:\n{code}"
        response = self.llm.generate(prompt)
        return [{"practice": line.strip()} for line in response.split("\n") if line.strip()]

    def assess_quality(self, code: str, language: str) -> dict:
        prompt = f"{CODE_REVIEW_PROMPT}\n\nLanguage: {language}\n\nCode:\n{code}"
        response = self.llm.generate(prompt)

        score = 5
        score_match = re.search(r"(?:score|rating)[:\s]*(\d+(?:\.\d+)?)", response, re.IGNORECASE)
        if score_match:
            score = float(score_match.group(1))
            score = max(0, min(10, score))

        return {"review": response, "quality_score": score, "language": language}
