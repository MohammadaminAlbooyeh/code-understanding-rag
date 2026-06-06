from backend.rag_system.prompts.bug_prompts import (
    BUG_DETECTION_PROMPT,
    SECURITY_PROMPT,
    PERFORMANCE_PROMPT,
)


class BugDetectionChain:
    def __init__(self, llm, prompt_manager):
        self.llm = llm
        self.prompt_manager = prompt_manager

    def detect_bugs(self, code: str, language: str) -> list[dict]:
        prompt = f"{BUG_DETECTION_PROMPT}\n\nLanguage: {language}\n\nCode:\n{code}"
        response = self.llm.generate(prompt)
        return [{"bug": line.strip()} for line in response.split("\n") if line.strip()]

    def detect_security_issues(self, code: str, language: str) -> list[dict]:
        prompt = f"{SECURITY_PROMPT}\n\nLanguage: {language}\n\nCode:\n{code}"
        response = self.llm.generate(prompt)
        return [{"issue": line.strip()} for line in response.split("\n") if line.strip()]

    def detect_performance_issues(self, code: str, language: str) -> list[dict]:
        prompt = f"{PERFORMANCE_PROMPT}\n\nLanguage: {language}\n\nCode:\n{code}"
        response = self.llm.generate(prompt)
        return [{"issue": line.strip()} for line in response.split("\n") if line.strip()]

    def detect_logic_errors(self, code: str, language: str) -> list[dict]:
        prompt = f"{BUG_DETECTION_PROMPT}\n\nFocus on logical errors and edge cases.\n\nLanguage: {language}\n\nCode:\n{code}"
        response = self.llm.generate(prompt)
        return [{"error": line.strip()} for line in response.split("\n") if line.strip()]
