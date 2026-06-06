class FunctionExtractor:
    def __init__(self):
        self.functions = []

    def extract(self, code: str, language: str) -> list[dict]:
        pass

    def extract_from_file(self, filepath: str) -> list[dict]:
        pass

    def get_function_details(self, func_name: str, code: str, language: str) -> dict:
        pass
