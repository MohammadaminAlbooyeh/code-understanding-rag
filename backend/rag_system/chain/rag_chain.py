class RAGChain:
    def __init__(self, retriever, llm, prompt_manager):
        self.retriever = retriever
        self.llm = llm
        self.prompt_manager = prompt_manager

    def run(self, query: str, code_id: str = None) -> str:
        pass

    def run_with_context(self, query: str, context: str) -> str:
        pass

    def run_stream(self, query: str, code_id: str = None):
        pass
