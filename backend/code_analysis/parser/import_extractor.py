class ImportExtractor:
    def __init__(self):
        self.imports = []

    def extract(self, code: str, language: str) -> list[dict]:
        pass

    def get_dependency_tree(self, imports: list[dict]) -> dict:
        pass
