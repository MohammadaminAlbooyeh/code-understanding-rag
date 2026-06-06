class ASTExtractor:
    def __init__(self):
        self.supported_languages = ["python", "javascript", "typescript", "java", "go", "cpp"]

    def extract(self, code: str, language: str) -> dict:
        pass

    def extract_from_file(self, filepath: str) -> dict:
        pass

    def get_ast_tree(self, code: str, language: str) -> str:
        pass
