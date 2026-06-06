class DocstringExtractor:
    def __init__(self):
        self.docstrings = []

    def extract(self, code: str, language: str) -> list[dict]:
        pass

    def extract_from_file(self, filepath: str) -> list[dict]:
        pass

    def format_docstring(self, docstring: str, format_type: str = "markdown") -> str:
        pass
