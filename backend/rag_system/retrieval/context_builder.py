class ContextBuilder:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens

    def build(self, retrieved_chunks: list[dict], query: str) -> str:
        pass

    def build_with_surrounding(self, chunk: dict, code: str) -> str:
        pass

    def build_multi_file_context(self, chunks: list[dict]) -> str:
        pass

    def truncate_context(self, context: str) -> str:
        pass
