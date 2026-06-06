from backend.rag_system.prompts.refactor_prompts import (
    REFACTOR_PROMPT,
    OPTIMIZATION_PROMPT,
    MODERNIZATION_PROMPT,
)


class RefactorChain:
    def __init__(self, llm, prompt_manager):
        self.llm = llm
        self.prompt_manager = prompt_manager

    def suggest_refactoring(self, code: str, language: str) -> list[dict]:
        prompt = f"{REFACTOR_PROMPT}\n\nLanguage: {language}\n\nCode:\n{code}"
        response = self.llm.generate(prompt)
        return [{"suggestion": line.strip()} for line in response.split("\n") if line.strip()]

    def suggest_optimizations(self, code: str, language: str) -> list[dict]:
        prompt = f"{OPTIMIZATION_PROMPT}\n\nLanguage: {language}\n\nCode:\n{code}"
        response = self.llm.generate(prompt)
        return [{"optimization": line.strip()} for line in response.split("\n") if line.strip()]

    def suggest_modernization(self, code: str, language: str) -> list[dict]:
        prompt = f"{MODERNIZATION_PROMPT}\n\nLanguage: {language}\n\nCode:\n{code}"
        response = self.llm.generate(prompt)
        return [{"suggestion": line.strip()} for line in response.split("\n") if line.strip()]

    def generate_refactored_code(self, code: str, suggestions: list[dict]) -> str:
        suggestions_text = "\n".join([str(s) for s in suggestions])
        prompt = f"""Refactor the following code based on the suggestions provided.

Original Code:
{code}

Suggestions:
{suggestions_text}

Please provide the complete refactored code."""
        return self.llm.generate(prompt)
