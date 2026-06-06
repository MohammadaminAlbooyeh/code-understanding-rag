class ExplanationChain:
    def __init__(self, llm, prompt_manager):
        self.llm = llm
        self.prompt_manager = prompt_manager

    def explain_code(self, code: str, language: str) -> str:
        pass

    def explain_function(self, func_data: dict) -> str:
        pass

    def explain_algorithm(self, code: str) -> str:
        pass

    def explain_concept(self, concept: str, code: str) -> str:
        pass
