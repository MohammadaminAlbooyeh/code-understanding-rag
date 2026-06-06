class ContextBuilder:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens

    def build(self, retrieved_chunks: list[dict], query: str) -> str:
        parts = []
        for i, chunk in enumerate(retrieved_chunks):
            meta = chunk.get("metadata", {})
            text = meta.get("text", chunk.get("text", ""))
            start = meta.get("start_line", chunk.get("start_line", "?"))
            end = meta.get("end_line", chunk.get("end_line", "?"))
            parts.append(f"--- Chunk {i} (lines {start}-{end}) ---\n{text}")
        context = "\n\n".join(parts)
        return self.truncate_context(context)

    def build_with_surrounding(self, chunk: dict, code: str) -> str:
        meta = chunk.get("metadata", {})
        text = meta.get("text", chunk.get("text", ""))
        start = meta.get("start_line", chunk.get("start_line", 1))
        end = meta.get("end_line", chunk.get("end_line", 1))

        lines = code.splitlines()
        surround_start = max(0, start - 6)
        surround_end = min(len(lines), end + 5)

        context_lines = lines[surround_start:surround_end]
        annotated = []
        for i, line in enumerate(context_lines, start=surround_start + 1):
            if start <= i <= end:
                annotated.append(f"> {line}")
            else:
                annotated.append(f"  {line}")

        context = "\n".join(annotated)
        return self.truncate_context(context)

    def build_multi_file_context(self, chunks: list[dict]) -> str:
        parts = []
        for chunk in chunks:
            meta = chunk.get("metadata", {})
            text = meta.get("text", chunk.get("text", ""))
            filename = meta.get("filename", chunk.get("filename", "unknown"))
            start = meta.get("start_line", chunk.get("start_line", "?"))
            end = meta.get("end_line", chunk.get("end_line", "?"))
            parts.append(f"--- File: {filename} Chunk {chunk.get('chunk_index', 0)} (lines {start}-{end}) ---\n{text}")
        context = "\n\n".join(parts)
        return self.truncate_context(context)

    def truncate_context(self, context: str) -> str:
        max_chars = self.max_tokens * 4
        if len(context) <= max_chars:
            return context
        truncated = context[:max_chars]
        last_space = truncated.rfind(" ")
        if last_space > 0:
            truncated = truncated[:last_space]
        return truncated + "..."
