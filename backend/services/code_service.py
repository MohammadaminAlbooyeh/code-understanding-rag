class CodeService:
    def __init__(self):
        self.storage = {}

    def upload(self, code: str, filename: str, language: str) -> dict:
        pass

    def get(self, code_id: str) -> dict:
        pass

    def list_all(self) -> list[dict]:
        pass

    def delete(self, code_id: str) -> bool:
        pass

    def get_languages(self) -> list[str]:
        pass
