class QAService:
    def __init__(self):
        pass

    def ask(self, code_id: str, question: str) -> dict:
        pass

    def get_history(self) -> list[dict]:
        pass

    def batch_ask(self, questions: list[dict]) -> list[dict]:
        pass

    def clear_history(self) -> None:
        pass
