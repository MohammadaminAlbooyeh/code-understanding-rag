class GroqLLM:
    def __init__(self, model: str = "mixtral-8x7b-32768", api_key: str = None):
        self.model = model
        self.api_key = api_key
        self.client = None

    def generate(self, prompt: str, **kwargs) -> str:
        pass

    def generate_stream(self, prompt: str, **kwargs):
        pass

    def generate_with_context(self, context: str, prompt: str, **kwargs) -> str:
        pass
