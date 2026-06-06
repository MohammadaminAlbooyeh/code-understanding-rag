class ReviewService:
    def __init__(self):
        pass

    def review_code(self, code_id: str) -> dict:
        pass

    def get_review(self, review_id: str) -> dict:
        pass

    def check_style(self, code_id: str) -> list[dict]:
        pass

    def check_security(self, code_id: str) -> list[dict]:
        pass
