class ReviewChain:
    def __init__(self, llm, prompt_manager):
        self.llm = llm
        self.prompt_manager = prompt_manager

    def review_code(self, code: str, language: str) -> dict:
        pass

    def check_style(self, code: str, language: str) -> list[dict]:
        pass

    def check_best_practices(self, code: str, language: str) -> list[dict]:
        pass

    def assess_quality(self, code: str, language: str) -> dict:
        pass
