class BugDetectionChain:
    def __init__(self, llm, prompt_manager):
        self.llm = llm
        self.prompt_manager = prompt_manager

    def detect_bugs(self, code: str, language: str) -> list[dict]:
        pass

    def detect_security_issues(self, code: str, language: str) -> list[dict]:
        pass

    def detect_performance_issues(self, code: str, language: str) -> list[dict]:
        pass

    def detect_logic_errors(self, code: str, language: str) -> list[dict]:
        pass
