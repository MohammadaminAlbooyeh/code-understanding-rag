from backend.rag_system.prompts.explanation_prompts import (
    EXPLAIN_CODE_PROMPT,
    EXPLAIN_FUNCTION_PROMPT,
    EXPLAIN_ALGORITHM_PROMPT,
)


class ExplanationChain:
    def __init__(self, llm, prompt_manager):
        self.llm = llm
        self.prompt_manager = prompt_manager

    def explain_code(self, code: str, language: str) -> str:
        prompt = f"{EXPLAIN_CODE_PROMPT}\n\nLanguage: {language}\n\nCode:\n{code}"
        return self.llm.generate(prompt)

    def explain_function(self, func_data: dict) -> str:
        prompt = f"{EXPLAIN_FUNCTION_PROMPT}\n\nFunction Data:\n{func_data}"
        return self.llm.generate(prompt)

    def explain_algorithm(self, code: str) -> str:
        prompt = f"{EXPLAIN_ALGORITHM_PROMPT}\n\nCode:\n{code}"
        return self.llm.generate(prompt)

    def explain_concept(self, concept: str, code: str) -> str:
        prompt = f"""Explain the concept of '{concept}' in the context of the following code.\n\nCode:\n{code}"""
        return self.llm.generate(prompt)
