class ChunkSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, code: str) -> list[dict]:
        chunks = []
        start = 0
        lines = code.splitlines(keepends=True)
        total_chars = len(code)
        chunk_index = 0

        while start < total_chars:
            end = min(start + self.chunk_size, total_chars)
            chunk_text = code[start:end]

            char_count = 0
            start_line = 1
            end_line = 1
            for i, line in enumerate(lines, start=1):
                prev = char_count
                char_count += len(line)
                if start >= prev and start < char_count:
                    start_line = i
                if end > prev and end <= char_count:
                    end_line = i
                    break
                if end >= total_chars and char_count >= total_chars:
                    end_line = i
                    break

            chunks.append({
                "text": chunk_text,
                "start_line": start_line,
                "end_line": end_line,
                "chunk_index": chunk_index,
                "total_chunks": None,
            })
            chunk_index += 1
            start += self.chunk_size - self.chunk_overlap

        for chunk in chunks:
            chunk["total_chunks"] = len(chunks)
        return chunks

    def split_by_function(self, parsed_code: dict) -> list[dict]:
        chunks = []
        functions = parsed_code.get("functions", [])
        code = parsed_code.get("code", "")
        lines = code.splitlines()
        for i, fn in enumerate(functions):
            start = max(0, fn.get("start_line", 1) - 2)
            end = min(len(lines), fn.get("end_line", len(lines)) + 1)
            chunk_text = "\n".join(lines[start:end])
            chunks.append({
                "text": chunk_text,
                "start_line": start + 1,
                "end_line": end,
                "chunk_index": i,
                "total_chunks": len(functions),
                "function_name": fn.get("name", ""),
            })
        return chunks

    def split_by_class(self, parsed_code: dict) -> list[dict]:
        chunks = []
        classes = parsed_code.get("classes", [])
        code = parsed_code.get("code", "")
        lines = code.splitlines()
        for i, cls in enumerate(classes):
            start = max(0, cls.get("start_line", 1) - 1)
            end = min(len(lines), cls.get("end_line", len(lines)))
            chunk_text = "\n".join(lines[start:end])
            chunks.append({
                "text": chunk_text,
                "start_line": start + 1,
                "end_line": end,
                "chunk_index": i,
                "total_chunks": len(classes),
                "class_name": cls.get("name", ""),
            })
        return chunks

    def split_by_lines(self, code: str, lines_per_chunk: int = 50) -> list[dict]:
        lines = code.splitlines()
        chunks = []
        for i in range(0, len(lines), lines_per_chunk):
            chunk_lines = lines[i:i + lines_per_chunk]
            chunks.append({
                "text": "\n".join(chunk_lines),
                "start_line": i + 1,
                "end_line": min(i + lines_per_chunk, len(lines)),
                "chunk_index": len(chunks),
                "total_chunks": None,
            })
        for chunk in chunks:
            chunk["total_chunks"] = len(chunks)
        return chunks
