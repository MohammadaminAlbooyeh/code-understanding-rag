from backend.rag_system.prompts.system_prompts import SYSTEM_PROMPT, CODE_ANALYSIS_PROMPT


class RAGChain:
    def __init__(self, retriever, llm, prompt_manager):
        self.retriever = retriever
        self.llm = llm
        self.prompt_manager = prompt_manager

    def run(self, query: str, code_id: str = None) -> str:
        context = ""
        if code_id:
            retrieved = self.retriever.retrieve(code_id)
            context = "\n".join([doc.page_content for doc in retrieved]) if retrieved else ""

        prompt = f"{SYSTEM_PROMPT}\n\n{CODE_ANALYSIS_PROMPT}\n\nContext:\n{context}\n\nQuery: {query}"
        return self.llm.generate(prompt)

    def run_with_context(self, query: str, context: str) -> str:
        prompt = f"{SYSTEM_PROMPT}\n\n{CODE_ANALYSIS_PROMPT}\n\nContext:\n{context}\n\nQuery: {query}"
        return self.llm.generate(prompt)

    def run_stream(self, query: str, code_id: str = None):
        context = ""
        if code_id:
            retrieved = self.retriever.retrieve(code_id)
            context = "\n".join([doc.page_content for doc in retrieved]) if retrieved else ""

        prompt = f"{SYSTEM_PROMPT}\n\n{CODE_ANALYSIS_PROMPT}\n\nContext:\n{context}\n\nQuery: {query}"
        for chunk in self.llm.generate_stream(prompt):
            yield chunk
