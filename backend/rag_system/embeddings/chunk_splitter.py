class ChunkSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, code: str) -> list[dict]:
        pass

    def split_by_function(self, parsed_code: dict) -> list[dict]:
        pass

    def split_by_class(self, parsed_code: dict) -> list[dict]:
        pass

    def split_by_lines(self, code: str, lines_per_chunk: int = 50) -> list[dict]:
        pass
