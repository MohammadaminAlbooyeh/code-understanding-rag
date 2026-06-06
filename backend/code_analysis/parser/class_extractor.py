class ClassExtractor:
    def __init__(self):
        self.classes = []

    def extract(self, code: str, language: str) -> list[dict]:
        pass

    def extract_from_file(self, filepath: str) -> list[dict]:
        pass

    def get_class_details(self, class_name: str, code: str, language: str) -> dict:
        pass
