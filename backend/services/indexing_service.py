class IndexingService:
    def __init__(self):
        pass

    def index_code(self, code_id: str) -> bool:
        pass

    def index_directory(self, directory: str) -> list[str]:
        pass

    def reindex(self, code_id: str) -> bool:
        pass

    def get_index_status(self, code_id: str) -> dict:
        pass
